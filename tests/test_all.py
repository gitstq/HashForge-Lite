#!/usr/bin/env python3
"""
HashForge Unit Tests
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import tempfile
from pathlib import Path

from hashforge.core import HashCalculator, Encoder, CryptoEngine, PasswordGenerator


class TestHashCalculator(unittest.TestCase):
    """Test HashCalculator class."""
    
    def test_sha256_hash(self):
        """Test SHA-256 hashing."""
        calc = HashCalculator('sha256')
        result = calc.hash_string('Hello World')
        expected = 'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e'
        self.assertEqual(result, expected)
    
    def test_md5_hash(self):
        """Test MD5 hashing."""
        calc = HashCalculator('md5')
        result = calc.hash_string('Hello World')
        expected = 'b10a8db164e0754105b7a99be72e3fe5'
        self.assertEqual(result, expected)
    
    def test_file_hash(self):
        """Test file hashing."""
        calc = HashCalculator('sha256')
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write('Hello World')
            temp_path = f.name
        
        try:
            result = calc.hash_file(temp_path)
            expected = 'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e'
            self.assertEqual(result, expected)
        finally:
            os.unlink(temp_path)
    
    def test_hash_all(self):
        """Test all hashes calculation."""
        calc = HashCalculator()
        result = calc.hash_all('test')
        self.assertIn('md5', result)
        self.assertIn('sha256', result)
        self.assertIn('sha512', result)
        self.assertEqual(len(result), 12)  # 12 algorithms
    
    def test_verify_hash(self):
        """Test hash verification."""
        calc = HashCalculator('sha256')
        expected = 'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e'
        self.assertTrue(calc.verify_hash('Hello World', expected))
        self.assertFalse(calc.verify_hash('Hello World', 'wrong_hash'))
    
    def test_invalid_algorithm(self):
        """Test invalid algorithm raises error."""
        with self.assertRaises(ValueError):
            HashCalculator('invalid_algo')


class TestEncoder(unittest.TestCase):
    """Test Encoder class."""
    
    def test_base64_encode_decode(self):
        """Test Base64 encoding and decoding."""
        encoder = Encoder()
        encoded = encoder.base64_encode('Hello World')
        self.assertEqual(encoded, 'SGVsbG8gV29ybGQ=')
        decoded = encoder.base64_decode(encoded)
        self.assertEqual(decoded, 'Hello World')
    
    def test_hex_encode_decode(self):
        """Test Hex encoding and decoding."""
        encoder = Encoder()
        encoded = encoder.hex_encode('Hello')
        self.assertEqual(encoded, '48656c6c6f')
        decoded = encoder.hex_decode(encoded)
        self.assertEqual(decoded, 'Hello')
    
    def test_url_encode_decode(self):
        """Test URL encoding and decoding."""
        encoder = Encoder()
        encoded = encoder.url_encode('Hello World')
        self.assertEqual(encoded, 'Hello%20World')
        decoded = encoder.url_decode(encoded)
        self.assertEqual(decoded, 'Hello World')
    
    def test_encode_all(self):
        """Test all encodings."""
        encoder = Encoder()
        result = encoder.encode_all('test')
        self.assertIn('base64', result)
        self.assertIn('hex', result)
        self.assertIn('url', result)
    
    def test_generic_encode_decode(self):
        """Test generic encode/decode methods."""
        encoder = Encoder()
        encoded = encoder.encode('Hello', 'base64')
        decoded = encoder.decode(encoded, 'base64')
        self.assertEqual(decoded, 'Hello')


class TestCryptoEngine(unittest.TestCase):
    """Test CryptoEngine class."""
    
    def test_xor_encrypt_decrypt(self):
        """Test XOR encryption and decryption."""
        crypto = CryptoEngine()
        encrypted = crypto.xor_encrypt('Hello', 'key')
        decrypted = crypto.xor_decrypt(encrypted, 'key')
        self.assertEqual(decrypted, 'Hello')
    
    def test_rot13(self):
        """Test ROT13 cipher."""
        crypto = CryptoEngine()
        result = crypto.rot13('Hello')
        self.assertEqual(result, 'Uryyb')
        # ROT13 is self-inverse
        self.assertEqual(crypto.rot13(result), 'Hello')
    
    def test_caesar_encrypt_decrypt(self):
        """Test Caesar cipher."""
        crypto = CryptoEngine()
        encrypted = crypto.caesar_encrypt('ABC', 3)
        self.assertEqual(encrypted, 'DEF')
        decrypted = crypto.caesar_decrypt(encrypted, 3)
        self.assertEqual(decrypted, 'ABC')
    
    def test_vigenere_encrypt_decrypt(self):
        """Test Vigenère cipher."""
        crypto = CryptoEngine()
        encrypted = crypto.vigenere_encrypt('HELLO', 'KEY')
        decrypted = crypto.vigenere_decrypt(encrypted, 'KEY')
        self.assertEqual(decrypted, 'HELLO')
    
    def test_generate_key(self):
        """Test key generation."""
        key1 = CryptoEngine.generate_key(32)
        key2 = CryptoEngine.generate_key(32)
        self.assertEqual(len(key1), 64)  # 32 bytes = 64 hex chars
        self.assertNotEqual(key1, key2)  # Keys should be different


class TestPasswordGenerator(unittest.TestCase):
    """Test PasswordGenerator class."""
    
    def test_generate_password(self):
        """Test password generation."""
        gen = PasswordGenerator()
        pwd = gen.generate(length=16)
        self.assertEqual(len(pwd), 16)
    
    def test_generate_password_no_symbols(self):
        """Test password without symbols."""
        gen = PasswordGenerator()
        pwd = gen.generate(length=20, symbols=False)
        self.assertEqual(len(pwd), 20)
        # Check no symbols
        import string
        symbols = set('!@#$%^&*()_+-=[]{}|;:,.<>?')
        self.assertFalse(any(c in symbols for c in pwd))
    
    def test_generate_passphrase(self):
        """Test passphrase generation."""
        gen = PasswordGenerator()
        pp = gen.generate_passphrase(word_count=4)
        words = pp.split('-')
        self.assertEqual(len(words), 4)
    
    def test_generate_pin(self):
        """Test PIN generation."""
        gen = PasswordGenerator()
        pin = gen.generate_pin(length=6)
        self.assertEqual(len(pin), 6)
        self.assertTrue(pin.isdigit())
    
    def test_analyze_password(self):
        """Test password analysis."""
        gen = PasswordGenerator()
        analysis = gen.analyze('MyStr0ng!Pass')
        self.assertEqual(analysis.length, 13)
        self.assertTrue(analysis.has_lowercase)
        self.assertTrue(analysis.has_uppercase)
        self.assertTrue(analysis.has_digits)
        self.assertTrue(analysis.has_symbols)
    
    def test_generate_multiple(self):
        """Test generating multiple passwords."""
        gen = PasswordGenerator()
        passwords = gen.generate_multiple(count=5)
        self.assertEqual(len(passwords), 5)
        # All passwords should be different
        self.assertEqual(len(set(passwords)), 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
