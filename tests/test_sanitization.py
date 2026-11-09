#!/usr/bin/env python3
"""Testes unitários para scripts/check_sanitization.py."""
import tempfile
import unittest
from pathlib import Path

from scripts.check_sanitization import check_file, is_luhn_valid


class TestSanitization(unittest.TestCase):
    def test_luhn_algorithm(self):
        # IMEI válido conhecido (Luhn válido)
        self.assertTrue(is_luhn_valid("352099001761481"))
        # Sequência inválida
        self.assertFalse(is_luhn_valid("352099001761482"))
        # Tamanho errado
        self.assertFalse(is_luhn_valid("12345"))

    def test_clean_file_passes(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".txt") as tmp:
            tmp.write("DeviceInfo: model=cancunf android=15 status=clean\n[REDACTED_MAC]\n")
            tmp.flush()
            violations = check_file(Path(tmp.name), set())
            self.assertEqual(violations, [])

    def test_mac_detection(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".txt") as tmp:
            tmp.write("wlan0: link/ether 00:1A:2B:3C:4D:5E brd ff:ff:ff:ff:ff:ff\n")
            tmp.flush()
            violations = check_file(Path(tmp.name), set())
            self.assertTrue(any("MAC exposto" in v for v in violations))

    def test_imei_detection(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".txt") as tmp:
            tmp.write("Device IMEI: 352099001761481 active slot 1\n")
            tmp.flush()
            violations = check_file(Path(tmp.name), set())
            self.assertTrue(any("IMEI válido detectado" in v for v in violations))

    def test_private_ip_and_allowlist(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".txt") as tmp:
            tmp.write('{"endpoint": "192.168.1.105"}\n')
            tmp.flush()
            path = Path(tmp.name)

            # Sem allowlist -> Falha
            violations = check_file(path, set())
            self.assertTrue(any("IP privado detectado" in v for v in violations))

            # Com allowlist -> Passa
            allowlist = {(str(path), "192.168.1.105")}
            violations = check_file(path, allowlist)
            self.assertEqual(violations, [])

    def test_account_name_detection(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".txt") as tmp:
            tmp.write("User Account {name=usuario.pessoal@gmail.com, type=com.google}\n")
            tmp.flush()
            violations = check_file(Path(tmp.name), set())
            self.assertTrue(any("Identificador de conta exposto" in v for v in violations))

    def test_phone_number_detection(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".txt") as tmp:
            tmp.write("Contato de suporte: (11) 98765-4321 no aparelho\n")
            tmp.flush()
            violations = check_file(Path(tmp.name), set())
            self.assertTrue(any("número de telefone" in v for v in violations))


if __name__ == "__main__":
    unittest.main()
