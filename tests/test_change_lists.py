#!/usr/bin/env python3
"""Testes de conformidade de listas de mudanças e registros de dados (C-1)."""

import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_change_lists import (
    check_snapshot_not_consumed_by_scripts,
    is_snapshot_or_candidate_file,
    load_audited_exceptions,
    load_notes_protected_packages,
    validate_data_disabled_lists,
)


class TestChangeListsAndDataSnapshots(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "data").mkdir(parents=True)
        (self.root / "scripts").mkdir(parents=True)
        (self.root / ".github/workflows").mkdir(parents=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_snapshot_with_protected_package_documented_in_notes_passes(self):
        """(a) Snapshot com protegido listado nas notas passa."""
        data_file = self.root / "data/test_disabled_packages.txt"
        data_file.write_text(
            "# SNAPSHOT DO APARELHO DE TESTE\ncom.android.emergency\ncom.example.bloat\n",
            encoding="utf-8",
        )
        notes_file = self.root / "data/test_disabled_packages.txt.notes.md"
        notes_file.write_text(
            "# Notas\n1. `com.android.emergency` — emergência histórica\n",
            encoding="utf-8",
        )
        protected = {"com.android.emergency"}

        checks, errors = validate_data_disabled_lists(self.root, protected)
        self.assertEqual(errors, [])
        self.assertGreater(checks, 0)

    def test_snapshot_with_protected_package_missing_from_notes_fails(self):
        """(b) Protegido sem nota falha."""
        data_file = self.root / "data/test_disabled_packages.txt"
        data_file.write_text(
            "# SNAPSHOT DO APARELHO DE TESTE\ncom.android.emergency\ncom.example.bloat\n",
            encoding="utf-8",
        )
        notes_file = self.root / "data/test_disabled_packages.txt.notes.md"
        notes_file.write_text(
            "# Notas\nNenhum pacote documentado aqui.\n",
            encoding="utf-8",
        )
        protected = {"com.android.emergency"}

        checks, errors = validate_data_disabled_lists(self.root, protected)
        self.assertTrue(any("com.android.emergency" in err and "sem documentação" in err for err in errors))

    def test_snapshot_missing_notes_file_fails(self):
        """Snapshot sem arquivo .notes.md falha."""
        data_file = self.root / "data/test_disabled_packages.txt"
        data_file.write_text(
            "# SNAPSHOT DO APARELHO DE TESTE\ncom.android.emergency\n",
            encoding="utf-8",
        )
        protected = {"com.android.emergency"}

        checks, errors = validate_data_disabled_lists(self.root, protected)
        self.assertTrue(any("requer notas em" in err for err in errors))

    def test_script_referencing_snapshot_file_fails(self):
        """(c) Um script que referencie o arquivo falha."""
        script_file = self.root / "scripts/malicious_runner.sh"
        script_file.write_text(
            "#!/bin/bash\ncat data/test_disabled_packages.txt | while read p; do echo $p; done\n",
            encoding="utf-8",
        )

        errors = check_snapshot_not_consumed_by_scripts(self.root, "test_disabled_packages.txt")
        self.assertTrue(any("faz referência indevida" in err for err in errors))

    # --- C-5 Audited Exceptions Tests ---

    def test_exception_missing_decided_by_fails(self):
        """Exceção sem 'decided_by' falha."""
        exc_file = self.root / "data/audited_exceptions.json"
        exc_file.write_text(json.dumps({
            "exceptions": [{
                "device": "reports/motorola/mock/disabled.txt",
                "package": "com.android.dialer",
                "status": "open",
                "reason": "motivo de teste",
                "decision_date": "2026-11-09",
                "functional_risk": "dialer"
            }]
        }), encoding="utf-8")

        exceptions_map, errors = load_audited_exceptions(self.root)
        self.assertTrue(any("decided_by" in err for err in errors))

    def test_exception_missing_functional_risk_fails(self):
        """Exceção sem 'functional_risk' falha."""
        exc_file = self.root / "data/audited_exceptions.json"
        exc_file.write_text(json.dumps({
            "exceptions": [{
                "device": "reports/motorola/mock/disabled.txt",
                "package": "com.android.dialer",
                "status": "open",
                "reason": "motivo de teste",
                "decided_by": "owner",
                "decision_date": "2026-11-09"
            }]
        }), encoding="utf-8")

        exceptions_map, errors = load_audited_exceptions(self.root)
        self.assertTrue(any("functional_risk" in err for err in errors))

    def test_exception_duplicate_fails(self):
        """Exceção duplicada falha."""
        exc_file = self.root / "data/audited_exceptions.json"
        exc_file.write_text(json.dumps({
            "exceptions": [
                {
                    "device": "reports/motorola/mock/disabled.txt",
                    "package": "com.android.dialer",
                    "status": "open",
                    "reason": "motivo 1",
                    "decided_by": "owner",
                    "decision_date": "2026-11-09",
                    "functional_risk": "dialer"
                },
                {
                    "device": "reports/motorola/mock/disabled.txt",
                    "package": "com.android.dialer",
                    "status": "open",
                    "reason": "motivo 2",
                    "decided_by": "owner",
                    "decision_date": "2026-11-09",
                    "functional_risk": "dialer"
                }
            ]
        }), encoding="utf-8")

        exceptions_map, errors = load_audited_exceptions(self.root)
        self.assertTrue(any("duplicada" in err for err in errors))

    def test_exception_valid_passes(self):
        """Exceção válida com todos os campos passa."""
        exc_file = self.root / "data/audited_exceptions.json"
        exc_file.write_text(json.dumps({
            "exceptions": [{
                "device": "reports/motorola/mock/disabled.txt",
                "package": "com.android.dialer",
                "status": "open",
                "reason": "motivo valido",
                "decided_by": "owner",
                "decision_date": "2026-11-09",
                "functional_risk": "dialer"
            }]
        }), encoding="utf-8")

        exceptions_map, errors = load_audited_exceptions(self.root)
        self.assertEqual(errors, [])
        self.assertIn(("reports/motorola/mock/disabled.txt", "com.android.dialer"), exceptions_map)

    def test_mitigated_exception_with_placeholder_role_holder_fails(self):
        """Exceção mitigada com 'not_tested' como role_holder falha."""
        from scripts.check_change_lists import validate_role_holders_for_risky_exceptions

        dev_dir = self.root / "reports/motorola/mock"
        dev_dir.mkdir(parents=True, exist_ok=True)
        func_file = dev_dir / "functional-tests.json"
        func_file.write_text(json.dumps({
            "role_holders": {"dialer": "not_tested"},
            "tests": []
        }), encoding="utf-8")

        exceptions_map = {
            ("reports/motorola/mock/changes/disabled.txt", "com.android.dialer"): {
                "status": "mitigated",
                "functional_risk": "dialer"
            }
        }
        checks, errors = validate_role_holders_for_risky_exceptions(self.root, exceptions_map)
        self.assertTrue(any("placeholder ou inválido" in err for err in errors))

    def test_mitigated_exception_with_valid_role_holder_and_passing_test_passes(self):
        """Exceção mitigada com titular válido e teste aprovado passa."""
        from scripts.check_change_lists import validate_role_holders_for_risky_exceptions

        dev_dir = self.root / "reports/motorola/mock"
        dev_dir.mkdir(parents=True, exist_ok=True)
        func_file = dev_dir / "functional-tests.json"
        func_file.write_text(json.dumps({
            "role_holders": {"dialer": "org.fossify.phone"},
            "tests": [{"test_name": "Telefonia", "status": "pass", "role": "dialer"}]
        }), encoding="utf-8")

        exceptions_map = {
            ("reports/motorola/mock/changes/disabled.txt", "com.android.dialer"): {
                "status": "mitigated",
                "functional_risk": "dialer"
            }
        }
        checks, errors = validate_role_holders_for_risky_exceptions(self.root, exceptions_map)
        self.assertEqual(errors, [])
        self.assertEqual(checks, 1)


if __name__ == "__main__":
    unittest.main()
