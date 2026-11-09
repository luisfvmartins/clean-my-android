"""Testes dos scripts ADB com executável simulado; nenhum aparelho físico é acessado."""
import json, os, subprocess, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DEBLOAT,RESTORE=ROOT/"scripts/debloat.sh",ROOT/"scripts/restore.sh"
PKG="com.example.optional"
FAKE=r'''#!/usr/bin/env python3
import json,os,sys
from pathlib import Path
p=Path(os.environ["FAKE_STATE"]); s=json.loads(p.read_text()); a=sys.argv[1:]
with Path(os.environ["FAKE_LOG"]).open("a") as f: f.write(json.dumps(a)+"\n")
if a==["devices"]:
 print("List of devices attached"); print(os.environ.get("FAKE_DEVICES","MOCK\tdevice")); raise SystemExit(0)
if len(a)<4 or a[0]!="-s" or a[2]!="shell": raise SystemExit(90)
c=a[3:]
if c[0]=="getprop":
 k=c[1]; print({"ro.product.model":os.getenv("FAKE_MODEL","Moto G54"),"ro.product.device":os.getenv("FAKE_DEVICE","cancunf"),"ro.build.product":os.getenv("FAKE_PRODUCT","cancunf"),"ro.build.version.release":os.getenv("FAKE_ANDROID","15")}.get(k,""))
elif c[:2]==["pm","path"]:
 if c[2] in s["installed"]: print("package:/data/app/"+c[2]+"/base.apk")
elif c[:3]==["pm","list","packages"]:
 if "-d" in c:
  for x in s["disabled"]: print("package:"+x)
elif c[:2]==["pm","disable-user"]:
 s["disabled"].append(c[-1]); p.write_text(json.dumps(s)); print("disabled")
elif c[:2]==["pm","enable"]:
 s["disabled"]=[x for x in s["disabled"] if x!=c[-1]]; p.write_text(json.dumps(s)); print("enabled")
else: raise SystemExit(91)
'''
class AdbScripts(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
  d=Path(self.tmp.name); b=d/"bin"; b.mkdir()
  adb=b/"adb"; adb.write_text(FAKE); adb.chmod(0o755)
  self.state_file,self.log=d/"state.json",d/"calls.log"; self.set_state([PKG],[])
  self.env=os.environ.copy()
  self.env.update(PATH=str(b)+os.pathsep+self.env.get("PATH",""),FAKE_STATE=str(self.state_file),FAKE_LOG=str(self.log),FAKE_DEVICES="MOCK\tdevice",FAKE_ANDROID="15",FAKE_DEVICE="cancunf",FAKE_PRODUCT="cancunf")
 def set_state(self,installed,disabled):
  self.state_file.write_text(json.dumps({"installed":installed,"disabled":disabled}))
 def state(self): return json.loads(self.state_file.read_text())
 def run_script(self,script,*args,answer=None):
  return subprocess.run(["bash",str(script),*args],input=answer,text=True,capture_output=True,env=self.env,timeout=10)
 def calls(self): return [json.loads(x) for x in self.log.read_text().splitlines()] if self.log.exists() else []
 def test_debloat_default_is_read_only(self):
  r=self.run_script(DEBLOAT); self.assertEqual(r.returncode,0,r.stderr); self.assertIn("somente leitura",r.stdout); self.assertEqual(self.state()["disabled"],[]); self.assertFalse(any("disable-user" in x for x in self.calls()))
 def test_debloat_rejects_no_device(self):
  self.env["FAKE_DEVICES"]=""; r=self.run_script(DEBLOAT); self.assertNotEqual(r.returncode,0); self.assertIn("exatamente um dispositivo",r.stderr)
 def test_debloat_rejects_multiple_devices(self):
  self.env["FAKE_DEVICES"]="A\tdevice\nB\tdevice"; r=self.run_script(DEBLOAT); self.assertNotEqual(r.returncode,0); self.assertIn("exatamente um dispositivo",r.stderr)
 def test_debloat_rejects_wrong_android(self):
  self.env["FAKE_ANDROID"]="14"; r=self.run_script(DEBLOAT,"--apply",PKG,answer=f"DESATIVAR {PKG}\n"); self.assertEqual(r.returncode,3); self.assertEqual(self.state()["disabled"],[])
 def test_debloat_rejects_invalid_and_protected_packages(self):
  self.assertEqual(self.run_script(DEBLOAT,"--apply","bad-name").returncode,2)
  r=self.run_script(DEBLOAT,"--apply","com.android.phone"); self.assertEqual(r.returncode,5); self.assertFalse(any("disable-user" in x for x in self.calls()))
 def test_debloat_cancel_does_not_change_state(self):
  r=self.run_script(DEBLOAT,"--apply",PKG,answer="NAO\n"); self.assertEqual(r.returncode,0); self.assertEqual(self.state()["disabled"],[])
 def test_debloat_requires_exact_confirmation(self):
  r=self.run_script(DEBLOAT,"--apply",PKG,answer=f"DESATIVAR {PKG}\n"); self.assertEqual(r.returncode,0,r.stderr); self.assertEqual(self.state()["disabled"],[PKG]); self.assertTrue(any("disable-user" in x for x in self.calls()))
 def test_restore_rejects_no_device(self):
  self.env["FAKE_DEVICES"]=""; r=self.run_script(RESTORE,PKG); self.assertNotEqual(r.returncode,0); self.assertIn("exatamente um dispositivo",r.stderr)
 def test_restore_does_not_change_enabled_package(self):
  r=self.run_script(RESTORE,PKG); self.assertEqual(r.returncode,0); self.assertEqual(self.state()["disabled"],[])
 def test_restore_cancel_does_not_change_state(self):
  self.set_state([PKG],[PKG]); r=self.run_script(RESTORE,PKG,answer="NAO\n"); self.assertEqual(r.returncode,0); self.assertEqual(self.state()["disabled"],[PKG])
 def test_restore_reenables_after_exact_confirmation(self):
  self.set_state([PKG],[PKG]); r=self.run_script(RESTORE,PKG,answer=f"REATIVAR {PKG}\n"); self.assertEqual(r.returncode,0,r.stderr); self.assertEqual(self.state()["disabled"],[]); self.assertTrue(any("enable" in x for x in self.calls()))
if __name__=="__main__": unittest.main()
