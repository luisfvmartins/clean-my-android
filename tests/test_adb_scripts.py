"""Testes dos scripts ADB com executável simulado; nenhum aparelho físico é acessado."""
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEBLOAT = ROOT / "scripts/debloat.sh"
RESTORE = ROOT / "scripts/restore.sh"
SNAPSHOT = ROOT / "scripts/snapshot.sh"
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
    # Mocking pm list packages flags
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
    if target not in s["disabled"]:
        s["disabled"].append(target)
    p.write_text(json.dumps(s))
    print(f"Package {target} new state: disabled-user")
elif c[:2] == ["pm", "enable"]:
    target = c[-1]
    s["disabled"] = [x for x in s["disabled"] if x != target]
    p.write_text(json.dumps(s))
    print(f"Package {target} new state: enabled")
elif c[0] == "dumpsys":
    if c[1] == "battery":
        print("Current Battery Service state:\n  level: 85\n  temperature: 280")
    elif c[1] == "meminfo":
        print("Total RAM: 8192MB\n Free RAM: 4200MB")
    elif c[1] == "package":
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
        self.env = os.environ.copy()
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
        return subprocess.run(
            ["bash", str(script), *args],
            input=answer,
            text=True,
            capture_output=True,
            env=self.env,
            timeout=10,
        )

    def calls(self):
        return [json.loads(x) for x in self.log.read_text().splitlines()] if self.log.exists() else []

    def test_debloat_default_is_read_only(self):
        r = self.run_script(DEBLOAT)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("somente leitura", r.stdout)
        self.assertEqual(self.state()["disabled"], [])
        self.assertFalse(any("disable-user" in x for x in self.calls()))

    def test_debloat_rejects_no_device(self):
        self.env["FAKE_DEVICES"] = ""
        r = self.run_script(DEBLOAT)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("exatamente um dispositivo", r.stderr)

    def test_debloat_rejects_multiple_devices(self):
        self.env["FAKE_DEVICES"] = "A\tdevice\nB\tdevice"
        r = self.run_script(DEBLOAT)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("exatamente um dispositivo", r.stderr)

    def test_debloat_rejects_wrong_android(self):
        self.env["FAKE_ANDROID"] = "14"
        r = self.run_script(DEBLOAT, "--apply", PKG, answer=f"DESATIVAR {PKG}\n")
        self.assertEqual(r.returncode, 3)
        self.assertEqual(self.state()["disabled"], [])

    def test_debloat_rejects_invalid_and_protected_packages(self):
        self.assertEqual(self.run_script(DEBLOAT, "--apply", "bad-name").returncode, 2)
        r = self.run_script(DEBLOAT, "--apply", "com.android.phone")
        self.assertEqual(r.returncode, 5)
        self.assertFalse(any("disable-user" in x for x in self.calls()))

    def test_debloat_cancel_does_not_change_state(self):
        r = self.run_script(DEBLOAT, "--apply", PKG, answer="NAO\n")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(self.state()["disabled"], [])

    def test_debloat_rejects_insufficient_homologation_level(self):
        # Remove override de catálogo para usar o catálogo padrão do repositório (nível 1 < 4)
        del self.env["CMA_DEVICE_CATALOG_FILE"]
        r = self.run_script(DEBLOAT, "--apply", PKG, answer=f"DESATIVAR {PKG}\n")
        self.assertEqual(r.returncode, 3)
        self.assertIn("gate de aplicação", r.stderr)
        self.assertEqual(self.state()["disabled"], [])

    def test_debloat_requires_exact_confirmation(self):
        self.env["CMA_DEVICE_CATALOG_FILE"] = str(self.mock_catalog)
        r = self.run_script(DEBLOAT, "--apply", PKG, answer=f"DESATIVAR {PKG}\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.state()["disabled"], [PKG])
        self.assertTrue(any("disable-user" in x for x in self.calls()))

    def test_debloat_writes_jsonl_log(self):
        self.env["CMA_DEVICE_CATALOG_FILE"] = str(self.mock_catalog)
        log_dir = Path(self.tmp.name) / "custom_logs"
        r = self.run_script(DEBLOAT, "--log-dir", str(log_dir), "--apply", PKG, answer=f"DESATIVAR {PKG}\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        actions_file = log_dir / "actions.jsonl"
        self.assertTrue(actions_file.exists())
        lines = actions_file.read_text().splitlines()
        self.assertEqual(len(lines), 1)
        entry = json.loads(lines[0])
        self.assertEqual(entry["action"], "disable")
        self.assertEqual(entry["package"], PKG)
        self.assertEqual(entry["verified_state"], "disabled")
        self.assertEqual(entry["rollback_command"], f"pm enable --user 0 {PKG}")

    def test_debloat_preflights_unwritable_log_dir(self):
        self.env["CMA_DEVICE_CATALOG_FILE"] = str(self.mock_catalog)
        unwritable_log = "/sys/kernel/debug/invalid_log_dir"
        r = self.run_script(DEBLOAT, "--log-dir", unwritable_log, "--apply", PKG, answer=f"DESATIVAR {PKG}\n")
        self.assertEqual(r.returncode, 4)
        self.assertEqual(self.state()["disabled"], [])

    def test_restore_rejects_no_device(self):
        self.env["FAKE_DEVICES"] = ""
        r = self.run_script(RESTORE, PKG)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("exatamente um dispositivo", r.stderr)

    def test_restore_does_not_change_enabled_package(self):
        r = self.run_script(RESTORE, PKG)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(self.state()["disabled"], [])

    def test_restore_cancel_does_not_change_state(self):
        self.set_state([PKG], [PKG])
        r = self.run_script(RESTORE, PKG, answer="NAO\n")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(self.state()["disabled"], [PKG])

    def test_restore_reenables_after_exact_confirmation(self):
        self.set_state([PKG], [PKG])
        r = self.run_script(RESTORE, PKG, answer=f"REATIVAR {PKG}\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.state()["disabled"], [])
        self.assertTrue(any("enable" in x for x in self.calls()))

    def test_restore_writes_jsonl_log(self):
        self.set_state([PKG], [PKG])
        log_dir = Path(self.tmp.name) / "restore_logs"
        r = self.run_script(RESTORE, "--log-dir", str(log_dir), PKG, answer=f"REATIVAR {PKG}\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        actions_file = log_dir / "actions.jsonl"
        self.assertTrue(actions_file.exists())
        lines = actions_file.read_text().splitlines()
        self.assertEqual(len(lines), 1)
        entry = json.loads(lines[0])
        self.assertEqual(entry["action"], "restore")
        self.assertEqual(entry["package"], PKG)
        self.assertEqual(entry["verified_state"], "enabled")

    def test_bilingual_cma_lang(self):
        # English
        self.env["CMA_LANG"] = "en"
        r_en = self.run_script(DEBLOAT)
        self.assertEqual(r_en.returncode, 0)
        self.assertIn("Read-only mode", r_en.stdout)
        self.assertIn("Usage:", r_en.stdout)

        # Portuguese
        self.env["CMA_LANG"] = "pt"
        r_pt = self.run_script(DEBLOAT)
        self.assertEqual(r_pt.returncode, 0)
        self.assertIn("Modo somente leitura", r_pt.stdout)
        self.assertIn("Uso:", r_pt.stdout)

    def test_exit_codes_documented_in_help(self):
        r_deb = self.run_script(DEBLOAT, "--help")
        self.assertEqual(r_deb.returncode, 0)
        for code in ["0:", "1:", "2:", "3:", "4:", "5:", "6:", "7:"]:
            self.assertIn(code, r_deb.stdout)

        r_res = self.run_script(RESTORE, "--help")
        self.assertEqual(r_res.returncode, 0)
        for code in ["0:", "1:", "2:", "3:", "4:"]:
            self.assertIn(code, r_res.stdout)

    def test_snapshot_script_success(self):
        out_dir = Path(self.tmp.name) / "snapshot_out"
        r = self.run_script(SNAPSHOT, "--label", "before", "--out", str(out_dir))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((out_dir / "device-info.txt").exists())
        self.assertTrue((out_dir / "packages-all.txt").exists())
        self.assertTrue((out_dir / "battery-summary.txt").exists())
        self.assertTrue((out_dir / "disk-usage.txt").exists())

    def test_snapshot_with_appops_collects_package_ops(self):
        out_dir = Path(self.tmp.name) / "snapshot_appops_out"
        r = self.run_script(SNAPSHOT, "--label", "before", "--out", str(out_dir), "--with-appops")
        self.assertEqual(r.returncode, 0, r.stderr)
        appops_file = out_dir / "appops.txt"
        self.assertTrue(appops_file.exists())
        self.assertIn("COARSE_LOCATION", appops_file.read_text())

    def test_snapshot_fails_on_adb_communication_error(self):
        self.env["FAKE_FAIL_ADB_CAPTURE"] = "1"
        out_dir = Path(self.tmp.name) / "snapshot_fail_out"
        r = self.run_script(SNAPSHOT, "--label", "before", "--out", str(out_dir))
        self.assertEqual(r.returncode, 3)

    def test_snapshot_script_invalid_args(self):
        r = self.run_script(SNAPSHOT)
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
