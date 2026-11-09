#!/usr/bin/env python3
"""Testes de conformidade de listas de mudanças e registros de dados (C-1)."""

import tempfile
import unittest
from pathlib import Path

from scripts.check_change_lists import (
    check_snapshot_not_consumed_by_scripts,
    is_snapshot_or_candidate_file,
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


if __name__ == "__main__":
    unittest.main()
