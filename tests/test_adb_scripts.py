"""Testes dos scripts ADB com executável simulado; nenhum aparelho físico é acessado."""
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEBLOAT = ROOT / "scripts/debloat.sh"
RESTORE = ROOT / "scripts/restore.sh"
SNAPSHOT = ROOT / "scripts/snapshot.sh"
PROTECTED_LIST = ROOT / "data/protected_essential_packages.txt"
PKG = "com.example.optional"

FAKE = r'''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path

p = Path(os.environ["FAKE_STATE"])
s = json.loads(p.read_text())
a = sys.argv[1:]

with Path(os.environ["FAKE_LOG"]).open("a") as f:
    f.write(json.dumps(a) + "\n")

if os.environ.get("FAKE_FAIL_ADB_CAPTURE") == "1" and len(a) >= 3 and a[0] == "-s" and a[2] == "shell":
    sys.exit(1)

if a == ["devices"] or a == ["devices", "-l"]:
    print("List of devices attached")
    print(os.environ.get("FAKE_DEVICES", "MOCK\tdevice"))
    sys.exit(0)

if len(a) < 4 or a[0] != "-s" or a[2] != "shell":
    sys.exit(90)

c = a[3:]

if c[0] == "getprop":
    k = c[1] if len(c) > 1 else ""
    prop_map = {
        "ro.product.model": os.getenv("FAKE_MODEL", "Moto G54 5G"),
        "ro.product.device": os.getenv("FAKE_DEVICE", "cancunf"),
        "ro.build.product": os.getenv("FAKE_PRODUCT", "cancunf"),
        "ro.build.version.release": os.getenv("FAKE_ANDROID", "15"),
        "ro.build.version.sdk": "35",
        "ro.build.version.security_patch": "2026-10-01",
        "ro.build.id": "AP4A.261005.001",
        "ro.build.type": "user"
    }
    print(prop_map.get(k, ""))
elif c[:2] == ["pm", "path"]:
    target = c[2]
    if target in s["installed"]:
        print("package:/data/app/" + target + "/base.apk")
elif c[:3] == ["pm", "list", "packages"]:
    flags = set(c[3:])
    for x in s["installed"]:
        if "-d" in flags:
            if x in s["disabled"]:
                print("package:" + x)
        elif "-e" in flags:
            if x not in s["disabled"]:
                print("package:" + x)
        else:
            print("package:" + x)
elif c[:2] == ["pm", "disable-user"]:
    target = c[-1]
    if os.environ.get("FAKE_FAIL_DISABLE") == "1":
        # Simulate command succeeded but package didn't stay disabled
        print(f"Package {target} disable error")
    else:
        if target not in s["disabled"]:
            s["disabled"].append(target)
        p.write_text(json.dumps(s))
        print(f"Package {target} new state: disabled-user")
elif c[:2] == ["pm", "enable"]:
    target = c[-1]
    if os.environ.get("FAKE_FAIL_ENABLE") == "1":
        print(f"Package {target} enable error")
    else:
        s["disabled"] = [x for x in s["disabled"] if x != target]
        p.write_text(json.dumps(s))
        print(f"Package {target} new state: enabled")
elif c[0] == "dumpsys":
    if c[1] == "battery":
        print("Current Battery Service state:\n  level: 85\n  temperature: 280")
    elif c[1] == "meminfo":
        print("Total RAM: 8192MB\n Free RAM: 4200MB")
    elif c[1] == "package":
        if os.environ.get("FAKE_LEAK_IMEI") == "1":
            # Valid Luhn 15-digit IMEI
            print("Device IMEI: 352099001761481")
        else:
            print("Packages permissions summary")
    else:
        print("dumpsys mock output")
elif c[:2] == ["df", "/data"]:
    print("Filesystem     1K-blocks      Used Available Use% Mounted on\n/dev/block/dm-0 120000000  40000000  80000000  34% /data")
elif c[:3] == ["cmd", "appops", "get"]:
    print("Uid mode: COARSE_LOCATION: allow")
else:
    sys.exit(91)
'''


class AdbScripts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        d = Path(self.tmp.name)
        b = d / "bin"
        b.mkdir()
        adb = b / "adb"
        adb.write_text(FAKE)
        adb.chmod(0o755)
        self.state_file, self.log = d / "state.json", d / "calls.log"
        self.set_state([PKG], [])

        mock_catalog = d / "mock_catalog.json"
        mock_catalog.write_text(json.dumps({
            "schema_version": 1,
            "devices": [
                {
                    "id": "motorola-moto-g54-5g",
                    "codename": "cancunf",
                    "model_code": "XT2343-1",
                    "homologation_level": 4,
                    "apply_supported": True
                }
            ]
        }))
        self.mock_catalog = mock_catalog

        self.env = os.environ.copy()
        self.env.update(
            PATH=str(b) + os.pathsep + self.env.get("PATH", ""),
            FAKE_STATE=str(self.state_file),
            FAKE_LOG=str(self.log),
            FAKE_DEVICES="MOCK\tdevice",
            FAKE_ANDROID="15",
            FAKE_DEVICE="cancunf",
            FAKE_PRODUCT="cancunf",
            CMA_LANG="pt",
            CMA_DEVICE_CATALOG_FILE=str(self.mock_catalog),
        )

    def set_state(self, installed, disabled):
        self.state_file.write_text(json.dumps({"installed": installed, "disabled": disabled}))

    def state(self):
        return json.loads(self.state_file.read_text())

    def run_script(self, script, *args, answer=None):
        bash_bin = os.environ.get("CMA_TEST_BASH")
        if not bash_bin:
            bash_bin = shutil.which("bash") or "/bin/bash"
        elif not os.path.isabs(bash_bin):
            bash_bin = shutil.which(bash_bin) or bash_bin
        return subprocess.run(
            [bash_bin, str(script), *args],
            input=answer,
            text=True,
            capture_output=True,
            env=self.env,
            timeout=10,
        )

    def calls(self):
        return [json.loads(x) for x in self.log.read_text().splitlines()] if self.log.exists() else []

    def get_no_adb_path(self) -> str:
        no_adb_dir = Path(self.tmp.name) / "no_adb_bin"
        if not no_adb_dir.exists():
            no_adb_dir.mkdir(parents=True, exist_ok=True)
            for sys_dir in ["/usr/bin", "/bin"]:
                p = Path(sys_dir)
                if not p.is_dir():
                    continue
                for item in p.iterdir():
                    if item.name == "adb":
                        continue
                    link = no_adb_dir / item.name
                    if not link.exists():
                        try:
                            link.symlink_to(item)
                        except OSError:
                            pass
        return str(no_adb_dir)

    # --- debloat.sh exit codes tests ---

    def test_debloat_code_0_read_only(self):
        r = self.run_script(DEBLOAT)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("somente leitura", r.stdout)
        self.assertEqual(self.state()["disabled"], [])

    def test_debloat_code_0_help(self):
        r = self.run_script(DEBLOAT, "--help")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Uso:", r.stdout)

    def test_debloat_code_0_cancel(self):
        r = self.run_script(DEBLOAT, "--apply", PKG, answer="NAO\n")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Cancelado", r.stdout)
        self.assertEqual(self.state()["disabled"], [])

    def test_debloat_code_0_already_disabled(self):
        self.set_state([PKG], [PKG])
        r = self.run_script(DEBLOAT, "--apply", PKG)
        self.assertEqual(r.returncode, 0)
        self.assertIn("já está desativado", r.stdout)

    def test_debloat_code_1_no_adb(self):
        self.env["PATH"] = self.get_no_adb_path()
        r = self.run_script(DEBLOAT)
        self.assertEqual(r.returncode, 1)
        self.assertIn("ADB", r.stderr)

    def test_debloat_code_1_no_device(self):
        self.env["FAKE_DEVICES"] = ""
        r = self.run_script(DEBLOAT)
        self.assertEqual(r.returncode, 1)
        self.assertIn("exatamente um dispositivo", r.stderr)

    def test_debloat_code_1_multiple_devices(self):
        self.env["FAKE_DEVICES"] = "DEV1\tdevice\nDEV2\tdevice"
        r = self.run_script(DEBLOAT)
        self.assertEqual(r.returncode, 1)
        self.assertIn("exatamente um dispositivo", r.stderr)

    def test_debloat_code_2_invalid_args(self):
        r = self.run_script(DEBLOAT, "--unknown-flag")
        self.assertEqual(r.returncode, 2)

    def test_debloat_code_2_invalid_package_syntax(self):
        r = self.run_script(DEBLOAT, "--apply", "invalid-package-name")
        self.assertEqual(r.returncode, 2)

    def test_debloat_code_3_unsupported_device_or_android(self):
        self.env["FAKE_DEVICE"] = "unsupported_phone"
        self.env["FAKE_PRODUCT"] = "unsupported_phone"
        r = self.run_script(DEBLOAT, "--apply", PKG)
        self.assertEqual(r.returncode, 3)

        self.env["FAKE_DEVICE"] = "cancunf"
        self.env["FAKE_PRODUCT"] = "cancunf"
        self.env["FAKE_ANDROID"] = "14"
        r2 = self.run_script(DEBLOAT, "--apply", PKG)
        self.assertEqual(r2.returncode, 3)

    def test_debloat_code_3_insufficient_homologation_level(self):
        # Remove catálogo simulado; usa o do repo com level 1 < 4
        del self.env["CMA_DEVICE_CATALOG_FILE"]
        r = self.run_script(DEBLOAT, "--apply", PKG, answer=f"DESATIVAR {PKG}\n")
        self.assertEqual(r.returncode, 3)
        self.assertIn("gate de aplicação", r.stderr)
        self.assertEqual(self.state()["disabled"], [])

    def test_debloat_code_4_unwritable_log_dir(self):
        unwritable_log = "/sys/kernel/debug/invalid_log_dir"
        r = self.run_script(DEBLOAT, "--log-dir", unwritable_log, "--apply", PKG, answer=f"DESATIVAR {PKG}\n")
        self.assertEqual(r.returncode, 4)
        self.assertEqual(self.state()["disabled"], [])

    def test_debloat_code_5_protected_package(self):
        r = self.run_script(DEBLOAT, "--apply", "com.android.phone")
        self.assertEqual(r.returncode, 5)
        self.assertIn("protegidos", r.stderr)

    def test_debloat_code_6_package_not_found(self):
        r = self.run_script(DEBLOAT, "--apply", "com.example.nonexistent")
        self.assertEqual(r.returncode, 6)

    def test_debloat_code_7_final_verification_failure(self):
        self.env["FAKE_FAIL_DISABLE"] = "1"
        r = self.run_script(DEBLOAT, "--apply", PKG, answer=f"DESATIVAR {PKG}\n")
        self.assertEqual(r.returncode, 7)

    def test_debloat_code_0_success_and_jsonl_log(self):
        log_dir = Path(self.tmp.name) / "custom_logs"
        r = self.run_script(DEBLOAT, "--log-dir", str(log_dir), "--apply", PKG, answer=f"DESATIVAR {PKG}\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.state()["disabled"], [PKG])

        actions_file = log_dir / "actions.jsonl"
        self.assertTrue(actions_file.exists())
        lines = actions_file.read_text().splitlines()
        self.assertEqual(len(lines), 1)
        entry = json.loads(lines[0])
        self.assertEqual(entry["action"], "disable")
        self.assertEqual(entry["package"], PKG)
        self.assertEqual(entry["verified_state"], "disabled")
        self.assertEqual(entry["rollback_command"], f"pm enable --user 0 {PKG}")

    # --- ALL 44 PROTECTED PACKAGES TEST ---

    def test_debloat_rejects_every_protected_package_with_code_5(self):
        protected_pkgs = [
            line.strip()
            for line in PROTECTED_LIST.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        ]
        self.assertGreaterEqual(len(protected_pkgs), 40)
        for p in protected_pkgs:
            r = self.run_script(DEBLOAT, "--apply", p)
            self.assertEqual(
                r.returncode,
                5,
                f"Pacote essencial protegido '{p}' não retornou exit code 5 (retornou {r.returncode}): {r.stderr}",
            )

    # --- restore.sh exit codes tests ---

    def test_restore_code_0_help(self):
        r = self.run_script(RESTORE, "--help")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Uso:", r.stdout)

    def test_restore_code_0_already_enabled(self):
        r = self.run_script(RESTORE, PKG)
        self.assertEqual(r.returncode, 0)
        self.assertIn("não consta como desativado", r.stdout)

    def test_restore_code_0_cancel(self):
        self.set_state([PKG], [PKG])
        r = self.run_script(RESTORE, PKG, answer="NAO\n")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(self.state()["disabled"], [PKG])

    def test_restore_code_1_no_adb(self):
        self.env["PATH"] = self.get_no_adb_path()
        r = self.run_script(RESTORE, PKG)
        self.assertEqual(r.returncode, 1)
        self.assertIn("ADB", r.stderr)

    def test_restore_code_1_device_count(self):
        self.env["FAKE_DEVICES"] = ""
        r = self.run_script(RESTORE, PKG)
        self.assertEqual(r.returncode, 1)

    def test_restore_code_2_invalid_args(self):
        r = self.run_script(RESTORE)
        self.assertEqual(r.returncode, 2)
        r2 = self.run_script(RESTORE, "not-a-valid-package")
        self.assertEqual(r2.returncode, 2)

    def test_restore_code_3_package_not_found(self):
        r = self.run_script(RESTORE, "com.example.nonexistent")
        self.assertEqual(r.returncode, 3)

    def test_restore_code_4_verification_failure(self):
        self.set_state([PKG], [PKG])
        self.env["FAKE_FAIL_ENABLE"] = "1"
        r = self.run_script(RESTORE, PKG, answer=f"REATIVAR {PKG}\n")
        self.assertEqual(r.returncode, 4)

    def test_restore_code_0_success_and_jsonl_log(self):
        self.set_state([PKG], [PKG])
        log_dir = Path(self.tmp.name) / "restore_logs"
        r = self.run_script(RESTORE, "--log-dir", str(log_dir), PKG, answer=f"REATIVAR {PKG}\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.state()["disabled"], [])

        actions_file = log_dir / "actions.jsonl"
        self.assertTrue(actions_file.exists())
        lines = actions_file.read_text().splitlines()
        self.assertEqual(len(lines), 1)
        entry = json.loads(lines[0])
        self.assertEqual(entry["action"], "restore")
        self.assertEqual(entry["package"], PKG)
        self.assertEqual(entry["verified_state"], "enabled")
        self.assertEqual(entry["rollback_command"], f"pm disable-user --user 0 {PKG}")

    # --- snapshot.sh tests ---

    def test_snapshot_code_0_success(self):
        out_dir = Path(self.tmp.name) / "snapshot_out"
        r = self.run_script(SNAPSHOT, "--label", "before", "--out", str(out_dir))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((out_dir / "device-info.txt").exists())
        self.assertTrue((out_dir / "packages-all.txt").exists())
        self.assertTrue((out_dir / "packages-enabled.txt").exists())
        self.assertTrue((out_dir / "packages-disabled.txt").exists())
        self.assertTrue((out_dir / "packages-system.txt").exists())
        self.assertTrue((out_dir / "packages-third-party.txt").exists())
        self.assertTrue((out_dir / "battery-summary.txt").exists())
        self.assertTrue((out_dir / "meminfo-summary.txt").exists())
        self.assertTrue((out_dir / "disk-usage.txt").exists())

    def test_snapshot_with_appops_collects_package_ops(self):
        out_dir = Path(self.tmp.name) / "snapshot_appops_out"
        r = self.run_script(SNAPSHOT, "--label", "before", "--out", str(out_dir), "--with-appops")
        self.assertEqual(r.returncode, 0, r.stderr)
        appops_file = out_dir / "appops.txt"
        self.assertTrue(appops_file.exists())
        self.assertIn("COARSE_LOCATION", appops_file.read_text())

    def test_snapshot_code_2_invalid_args(self):
        r = self.run_script(SNAPSHOT)
        self.assertEqual(r.returncode, 2)
        r2 = self.run_script(SNAPSHOT, "--label", "invalid_label", "--out", "/tmp/out")
        self.assertEqual(r2.returncode, 2)

    def test_snapshot_code_3_adb_communication_failure(self):
        self.env["FAKE_FAIL_ADB_CAPTURE"] = "1"
        out_dir = Path(self.tmp.name) / "fail_capture_out"
        r = self.run_script(SNAPSHOT, "--label", "before", "--out", str(out_dir))
        self.assertEqual(r.returncode, 3)
        self.assertIn("comunicação", r.stderr)

    def test_snapshot_code_5_sanitization_leak_aborts(self):
        self.env["FAKE_LEAK_IMEI"] = "1"
        out_dir = Path(self.tmp.name) / "leak_out"
        r = self.run_script(SNAPSHOT, "--label", "before", "--out", str(out_dir), "--with-permissions")
        self.assertEqual(r.returncode, 5)
        # Verify output directory was NOT populated
        self.assertFalse((out_dir / "device-info.txt").exists())

    # --- Bilingual and Exit Codes Docs tests ---

    def test_bilingual_cma_lang(self):
        self.env["CMA_LANG"] = "en"
        r_en = self.run_script(DEBLOAT)
        self.assertEqual(r_en.returncode, 0)
        self.assertIn("Read-only mode", r_en.stdout)

        self.env["CMA_LANG"] = "pt"
        r_pt = self.run_script(DEBLOAT)
        self.assertEqual(r_pt.returncode, 0)
        self.assertIn("Modo somente leitura", r_pt.stdout)

    def test_exit_codes_documented_in_help(self):
        r_deb = self.run_script(DEBLOAT, "--help")
        self.assertEqual(r_deb.returncode, 0)
        for code in ["0:", "1:", "2:", "3:", "4:", "5:", "6:", "7:"]:
            self.assertIn(code, r_deb.stdout)

        r_res = self.run_script(RESTORE, "--help")
        self.assertEqual(r_res.returncode, 0)
        for code in ["0:", "1:", "2:", "3:", "4:"]:
            self.assertIn(code, r_res.stdout)


if __name__ == "__main__":
    unittest.main()
