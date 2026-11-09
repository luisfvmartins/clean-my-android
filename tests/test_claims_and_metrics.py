#!/usr/bin/env python3
"""Testes automatizados para validação de alegações técnicas e métricas (PT-1)."""

import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_claims import validate_claims, validate_metrics_json


class TestClaimsAndMetricsValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "docs").mkdir(parents=True)
        (self.root / "data").mkdir(parents=True)
        (self.root / "reports/motorola/test-device").mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_unqualified_absolute_term_fails(self) -> None:
        doc = self.root / "docs/audit.md"
        doc.write_text("O procedimento elimina completamente o rastreamento de dados.\n", encoding="utf-8")
        allowlist = self.root / "data/claims_allowlist.json"
        allowlist.write_text(json.dumps({"entries": []}), encoding="utf-8")

        checks, errors = validate_claims(self.root, allowlist)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("elimina" in err for err in errors))

    def test_qualified_term_with_marker_passes(self) -> None:
        doc = self.root / "docs/audit.md"
        doc.write_text("O procedimento desativa o pacote (efeito sobre rastreamento: não medido).\n", encoding="utf-8")
        allowlist = self.root / "data/claims_allowlist.json"
        allowlist.write_text(json.dumps({"entries": []}), encoding="utf-8")

        checks, errors = validate_claims(self.root, allowlist)
        self.assertEqual(len(errors), 0)

    def test_term_with_evidence_link_passes(self) -> None:
        doc = self.root / "docs/audit.md"
        doc.write_text("Classificação de adware fundamentada em [evidência](evidence.txt).\n", encoding="utf-8")
        allowlist = self.root / "data/claims_allowlist.json"
        allowlist.write_text(json.dumps({"entries": []}), encoding="utf-8")

        checks, errors = validate_claims(self.root, allowlist)
        self.assertEqual(len(errors), 0)

    def test_allowlisted_term_passes(self) -> None:
        doc = self.root / "docs/audit.md"
        doc.write_text("Rastreamento do Sistema (ferramenta AOSP de depuração)\n", encoding="utf-8")
        allowlist = self.root / "data/claims_allowlist.json"
        allowlist.write_text(json.dumps({
            "entries": [{
                "path": "docs/audit.md",
                "line": 1,
                "term": "Rastreamento",
                "category": "A",
                "rationale": "Nome oficial da ferramenta AOSP"
            }]
        }), encoding="utf-8")

        checks, errors = validate_claims(self.root, allowlist)
        self.assertEqual(len(errors), 0)

    def test_old_comparativo_schema_fails(self) -> None:
        # Schema antigo livre do A30s sem kind, status, method, evidence
        comp = self.root / "reports/motorola/test-device/comparativo.json"
        comp.write_text(json.dumps({
            "device": "Test Device",
            "metrics": [
                {
                    "indicator": "Pacotes Desativados",
                    "before": "0",
                    "after": "46"
                }
            ]
        }), encoding="utf-8")

        checks, errors = validate_metrics_json(self.root)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("kind inválido" in err for err in errors))

    def test_canonical_comparativo_schema_passes(self) -> None:
        evidence_file = self.root / "reports/motorola/test-device/packages.txt"
        evidence_file.write_text("package:com.example.app\n", encoding="utf-8")

        comp = self.root / "reports/motorola/test-device/comparativo.json"
        comp.write_text(json.dumps({
            "device": "Test Device",
            "metrics": [
                {
                    "indicator": "Pacotes Desativados",
                    "kind": "count",
                    "status": "measured",
                    "method": "pm list packages -d",
                    "before": "0",
                    "after": "46",
                    "evidence": ["reports/motorola/test-device/packages.txt"],
                    "limitations": "Contagem direta via ADB."
                }
            ]
        }), encoding="utf-8")

        checks, errors = validate_metrics_json(self.root)
        self.assertEqual(len(errors), 0)

    def test_count_metric_claiming_effect_fails(self) -> None:
        evidence_file = self.root / "reports/motorola/test-device/packages.txt"
        evidence_file.write_text("package:com.example.app\n", encoding="utf-8")

        comp = self.root / "reports/motorola/test-device/comparativo.json"
        comp.write_text(json.dumps({
            "device": "Test Device",
            "metrics": [
                {
                    "indicator": "Pacotes Removidos",
                    "kind": "count",
                    "status": "measured",
                    "method": "pm list packages",
                    "variation": "46 pacotes com economia de bateria",
                    "evidence": ["reports/motorola/test-device/packages.txt"],
                    "limitations": "Contagem direta via ADB."
                }
            ]
        }), encoding="utf-8")

        checks, errors = validate_metrics_json(self.root)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("métrica do tipo 'count' não pode alegar efeito" in err for err in errors))

    def test_measured_status_missing_evidence_fails(self) -> None:
        comp = self.root / "reports/motorola/test-device/comparativo.json"
        comp.write_text(json.dumps({
            "device": "Test Device",
            "metrics": [
                {
                    "indicator": "Memória RAM",
                    "kind": "resource",
                    "status": "measured",
                    "method": "dumpsys meminfo",
                    "evidence": [],
                    "limitations": "Nenhuma."
                }
            ]
        }), encoding="utf-8")

        checks, errors = validate_metrics_json(self.root)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("com status=measured exige lista 'evidence' não vazia" in err for err in errors))


if __name__ == "__main__":
    unittest.main()
