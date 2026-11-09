#!/usr/bin/env python3
"""Testes de conformidade de layout canônico por nível de homologação (PT-5)."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestCanonicalLayout(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_current_repository_devices_satisfy_layout(self) -> None:
        catalog_path = ROOT / "data/device_catalog.json"
        self.assertTrue(catalog_path.is_file())
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))

        for device in catalog.get("devices", []):
            device_id = device.get("id")
            level = device.get("homologation_level")
            report_path = device.get("report")
            self.assertIsNotNone(report_path)
            dev_dir = (ROOT / report_path).parent

            # Level 1 mandatory files
            level_1 = [
                "README.md",
                "README.en.md",
                "audit.md",
                "audit.en.md",
                "metrics.json",
                "functional-tests.json",
            ]
            for f in level_1:
                p = dev_dir / f
                self.assertTrue(p.is_file(), f"{device_id} missing {f}")
                self.assertGreater(p.stat().st_size, 0, f"{device_id} has empty {f}")

            # before inventory
            self.assertTrue(
                (dev_dir / "before/inventory.json").is_file()
                or (dev_dir / "before/packages.txt").is_file()
                or (dev_dir / "before/packages-initial.txt").is_file(),
                f"{device_id} missing before inventory",
            )

            if level >= 2:
                level_2 = [
                    "comparison-report.md",
                    "comparison-report.en.md",
                    "changes/change-log.md",
                    "changes/change-log.en.md",
                ]
                for f in level_2:
                    p = dev_dir / f
                    self.assertTrue(p.is_file(), f"{device_id} missing {f}")
                    self.assertGreater(p.stat().st_size, 0, f"{device_id} has empty {f}")

                self.assertTrue(
                    (dev_dir / "after/inventory.json").is_file()
                    or (dev_dir / "after/packages.txt").is_file()
                    or (dev_dir / "after/packages-final.txt").is_file(),
                    f"{device_id} missing after inventory",
                )

                if (dev_dir / "changes").is_dir():
                    self.assertTrue((dev_dir / "changes/disabled-packages.txt").is_file())
                    self.assertTrue((dev_dir / "changes/removed-packages.txt").is_file())

    def test_missing_level_1_file_is_detected(self) -> None:
        # Replicate minimal device directory
        dev_dir = self.test_root / "reports/motorola/mock-device"
        dev_dir.mkdir(parents=True, exist_ok=True)
        (dev_dir / "README.md").write_text("# Mock", encoding="utf-8")
        (dev_dir / "README.en.md").write_text("# Mock", encoding="utf-8")
        # Missing audit.md and metrics.json
        level_1 = ["README.md", "README.en.md", "audit.md", "audit.en.md", "metrics.json", "functional-tests.json"]
        missing = [f for f in level_1 if not (dev_dir / f).is_file()]
        self.assertIn("audit.md", missing)
        self.assertIn("metrics.json", missing)


if __name__ == "__main__":
    unittest.main()
