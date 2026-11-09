#!/usr/bin/env python3
"""Testes unitários para scripts/check_sanitization.py."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.check_sanitization import (
    check_file,
    check_image_metadata,
    is_luhn_valid,
    load_allowlist,
    scan_target,
)


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
            # Garante que o valor real não é vazado na mensagem
            self.assertFalse(any("00:1A:2B:3C:4D:5E" in v for v in violations))

    def test_imei_detection(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".txt") as tmp:
            tmp.write("Device IMEI: 352099001761481 active slot 1\n")
            tmp.flush()
            violations = check_file(Path(tmp.name), set())
            self.assertTrue(any("IMEI válido detectado" in v for v in violations))
            self.assertFalse(any("352099001761481" in v for v in violations))

    def test_private_ip_and_allowlist(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".txt") as tmp:
            tmp.write('{"endpoint": "192.168.1.105"}\n')
            tmp.flush()
            path = Path(tmp.name)

            # Sem allowlist -> Falha
            violations = check_file(path, set())
            self.assertTrue(any("IP privado" in v for v in violations))
            self.assertFalse(any("192.168.1.105" in v for v in violations))

            # Com allowlist -> Passa
            allowlist = {(str(path), "192.168.1.105")}
            violations = check_file(path, allowlist)
            self.assertEqual(violations, [])

    def test_ipv6_private_detection(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".txt") as tmp:
            tmp.write("Interface wlan0 inet6 fe80::1ff:fe00:3a60/64 scope link\n")
            tmp.write("Interface tun0 inet6 fd12:3456:789a:1::1/64 scope global\n")
            tmp.flush()
            path = Path(tmp.name)
            violations = check_file(path, set())
            self.assertTrue(any("IPv6 privado detectado" in v for v in violations))
            self.assertFalse(any("fe80::1ff:fe00:3a60" in v for v in violations))

    def test_account_name_detection(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".txt") as tmp:
            tmp.write("User Account {name=usuario.pessoal@gmail.com, type=com.google}\n")
            tmp.flush()
            violations = check_file(Path(tmp.name), set())
            self.assertTrue(any("Identificador de conta" in v for v in violations))
            self.assertFalse(any("usuario.pessoal@gmail.com" in v for v in violations))

    def test_email_with_long_tld(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".txt") as tmp:
            tmp.write("Contato corporativo: admin@auditoria.technology no servidor\n")
            tmp.flush()
            violations = check_file(Path(tmp.name), set())
            self.assertTrue(any("e-mail" in v.lower() for v in violations))
            self.assertFalse(any("admin@auditoria.technology" in v for v in violations))

    def test_phone_number_mobile_and_landline(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".txt") as tmp:
            tmp.write("Celular: (11) 98765-4321 no aparelho\n")
            tmp.write("Fixo: (11) 2345-6789 no escritório\n")
            tmp.write("Tamanho de arquivo: apkBytes: 202552832\n")  # Falso positivo prevenido
            tmp.flush()
            violations = check_file(Path(tmp.name), set())
            self.assertTrue(any("telefone celular" in v for v in violations))
            self.assertTrue(any("telefone fixo" in v for v in violations))
            # Garantir que apkBytes não gerou falso positivo
            self.assertEqual(len(violations), 2)

    def test_credentials_detection(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".txt") as tmp:
            tmp.write('api_key: "abc123xyz789SECRET_VALUE"\n')
            tmp.write('Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0\n')
            tmp.write('api_key: "sua_api_key"\n')  # Placeholder dummy não deve falhar
            tmp.flush()
            violations = check_file(Path(tmp.name), set())
            self.assertTrue(any("Credencial ou token" in v for v in violations))
            self.assertTrue(any("Token Bearer" in v for v in violations))
            self.assertEqual(len(violations), 2)
            self.assertFalse(any("abc123xyz789SECRET_VALUE" in v for v in violations))

    def test_scan_single_file_target(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".txt") as tmp:
            tmp.write("192.168.0.1\n")
            tmp.flush()
            violations = scan_target(Path(tmp.name), set())
            self.assertTrue(len(violations) >= 1)

    def test_image_metadata_png(self):
        # Cria um PNG mínimo com chunk tEXt
        png_header = b"\x89PNG\r\n\x1a\n"
        # IHDR chunk
        ihdr_data = b"\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00"
        ihdr_chunk = len(ihdr_data).to_bytes(4, "big") + b"IHDR" + ihdr_data + b"\x00\x00\x00\x00"
        # tEXt chunk
        text_data = b"Comment\x00Sensitive screenshot info"
        text_chunk = len(text_data).to_bytes(4, "big") + b"tEXt" + text_data + b"\x00\x00\x00\x00"
        # IEND chunk
        iend_chunk = b"\x00\x00\x00\x00IEND\xaeB`\x82"
        raw_png = png_header + ihdr_chunk + text_chunk + iend_chunk

        with tempfile.NamedTemporaryFile("wb", suffix=".png") as tmp:
            tmp.write(raw_png)
            tmp.flush()
            violations = check_image_metadata(Path(tmp.name))
            self.assertTrue(any("Metadados ancilares/EXIF" in v for v in violations))

    def test_image_metadata_jpeg(self):
        # Mock JPEG com marcador APP1 e Exif
        raw_jpeg = b"\xff\xd8\xff\xe1\x00\x10Exif\x00\x00data\xff\xd9"
        with tempfile.NamedTemporaryFile("wb", suffix=".jpg") as tmp:
            tmp.write(raw_jpeg)
            tmp.flush()
            violations = check_image_metadata(Path(tmp.name))
            self.assertTrue(any("Metadados EXIF" in v for v in violations))

    def test_corrupt_allowlist_handling(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".json") as tmp:
            tmp.write("INVALID JSON {")
            tmp.flush()
            with patch("scripts.check_sanitization.ALLOWLIST_PATH", Path(tmp.name)):
                _, ok = load_allowlist()
                self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
