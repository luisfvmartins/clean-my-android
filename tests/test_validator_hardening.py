#!/usr/bin/env python3
"""Testes de endurecimento das verificações estáticas do validador (C-6).

Regras verificadas:
1. Alegações em inglês não qualificadas (privacy gain, verified, confirmed, etc.).
2. 'Tested in CI' exige SO em active workflows (.github/workflows/).
3. QUALITY_SCORECARD exige artefato existente em docs/evidence-runs/** para cada linha Met/Atendido.
4. SELF_AUDIT rejeita 'Agree' e fontes genéricas sem caminho no repositório ou URL.
"""

import tempfile
import unittest
from pathlib import Path

from scripts.check_claims import (
    validate_ci_platform_claims,
    validate_claims,
    validate_scorecard_evidence_references,
    validate_self_audit_rigor,
)


class TestValidatorHardening(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "docs").mkdir(parents=True)
        (self.root / "data").mkdir(parents=True)
        (self.root / ".github/workflows").mkdir(parents=True)
        # Empty allowlist
        (self.root / "data/claims_allowlist.json").write_text('{"entries": []}', encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    # Rule 1: Claims (English terms)
    def test_english_claim_unqualified_fails(self):
        """Termo em inglês não qualificado (e.g. 'verified', 'highly recommended') falha."""
        doc = self.root / "docs/sample.md"
        doc.write_text("This debloat was verified and is highly recommended.\n", encoding="utf-8")
        checks, errors = validate_claims(self.root, self.root / "data/claims_allowlist.json")
        self.assertTrue(any("verified" in err or "highly recommended" in err for err in errors))

    def test_english_claim_qualified_passes(self):
        """Termo em inglês qualificado com marcador [evidence](url) ou (hypothesis) passa."""
        doc = self.root / "docs/sample.md"
        doc.write_text("This result has [verified](docs/evidence.md) status (hypothesis).\n", encoding="utf-8")
        checks, errors = validate_claims(self.root, self.root / "data/claims_allowlist.json")
        self.assertEqual(errors, [])

    # Rule 2: 'Tested in CI'
    def test_tested_in_ci_without_os_in_active_workflows_fails(self):
        """'Tested in CI (macos-latest)' falha se workflow ativo só tem ubuntu-latest."""
        wf = self.root / ".github/workflows/validate.yml"
        wf.write_text("jobs:\n  test:\n    runs-on: ubuntu-latest\n", encoding="utf-8")
        doc = self.root / "docs/PLATFORMS.md"
        doc.write_text("macOS: Tested in CI (macos-latest)\n", encoding="utf-8")

        checks, errors = validate_ci_platform_claims(self.root)
        self.assertTrue(any("macos-latest" in err and "não está presente em workflows ativos" in err for err in errors))

    def test_tested_in_ci_with_matching_active_workflow_passes(self):
        """'Tested in CI (ubuntu-latest)' passa se workflow ativo tem ubuntu-latest."""
        wf = self.root / ".github/workflows/validate.yml"
        wf.write_text("jobs:\n  test:\n    runs-on: ubuntu-latest\n", encoding="utf-8")
        doc = self.root / "docs/PLATFORMS.md"
        doc.write_text("Linux: Tested in CI (ubuntu-latest)\n", encoding="utf-8")

        checks, errors = validate_ci_platform_claims(self.root)
        self.assertEqual(errors, [])

    # Rule 3: Scorecard evidence references
    def test_scorecard_met_missing_evidence_artifact_fails(self):
        """Linha Met sem artefato correspondente em docs/evidence-runs/** falha."""
        scorecard = self.root / "docs/QUALITY_SCORECARD.md"
        scorecard.write_text(
            "| Portability | Met | `python3 test.py` | [evidence](docs/evidence-runs/2026-11-09/missing.txt) |\n",
            encoding="utf-8",
        )
        checks, errors = validate_scorecard_evidence_references(self.root)
        self.assertTrue(any("missing.txt" in err and "não existe" in err for err in errors))

    def test_scorecard_met_with_existing_evidence_artifact_passes(self):
        """Linha Met com artefato existente em docs/evidence-runs/** passa."""
        evidence_dir = self.root / "docs/evidence-runs/2026-11-09"
        evidence_dir.mkdir(parents=True)
        artifact = evidence_dir / "check_01.txt"
        artifact.write_text("exit_code: 0\n", encoding="utf-8")

        scorecard = self.root / "docs/QUALITY_SCORECARD.md"
        scorecard.write_text(
            "| Portability | Met | `python3 test.py` | [evidence](docs/evidence-runs/2026-11-09/check_01.txt) |\n",
            encoding="utf-8",
        )
        checks, errors = validate_scorecard_evidence_references(self.root)
        self.assertEqual(errors, [])

    # Rule 4: Self-audit rigor
    def test_self_audit_with_agree_or_generic_source_fails(self):
        """Autoauditoria com 'Agree' ou fonte genérica falha."""
        audit_file = self.root / "docs/SELF_AUDIT_2026-11-09.md"
        audit_file.write_text(
            "| com.example.pkg | Moto G54 | Agree | Motorola Firmware / Dumpsys |\n",
            encoding="utf-8",
        )
        checks, errors = validate_self_audit_rigor(self.root)
        self.assertTrue(any("Agree" in err or "genérica" in err for err in errors))

    def test_self_audit_with_grounded_verdict_and_evidence_path_passes(self):
        """Autoauditoria com veredito suportado e evidência em arquivo do repo passa."""
        evidence = self.root / "docs/evidence.txt"
        evidence.write_text("dump\n", encoding="utf-8")

        audit_file = self.root / "docs/SELF_AUDIT_2026-11-09.md"
        audit_file.write_text(
            "| com.example.pkg | Moto G54 | supported-by-repo-data | [evidence](docs/evidence.txt) |\n",
            encoding="utf-8",
        )
        checks, errors = validate_self_audit_rigor(self.root)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
