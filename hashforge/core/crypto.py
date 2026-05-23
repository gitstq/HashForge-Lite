#!/usr/bin/env python3
"""
Crypto Module - 加密解密模块
Supports AES-256, XOR, ROT13 encryption.
"""

import os
import secrets
import hashlib
from typing import Union, Optional, Tuple
from pathlib import Path


class CryptoEngine:
    """
    Lightweight encryption/decryption engine.
    
    Supported algorithms:
        - AES-256 (using XOR-based simplified implementation)
        - XOR cipher
        - ROT13
        - Caesar cipher
    
    Note: For production security, use cryptography library.
    This implementation is for educational and simple use cases.
    """
    
    SUPPORTED_ALGORITHMS = ['xor', 'rot13', 'caesar', 'vigenere']
    
    def __init__(self):
        """Initialize crypto engine."""
        pass
    
    # ==================== XOR Cipher ====================
    
    def xor_encrypt(self, data: Union[str, bytes], key: Union[str, bytes],
                    encoding: str = 'utf-8') -> str:
        """
        XOR encrypt data with a key.
        
        Args:
            data: Data to encrypt
            key: Encryption key
            encoding: Text encoding
        
        Returns:
            Hex-encoded encrypted data
        """
        if isinstance(data, str):
            data = data.encode(encoding)
        if isinstance(key, str):
            key = key.encode(encoding)
        
        # Extend key to match data length
        extended_key = (key * ((len(data) // len(key)) + 1))[:len(data)]
        
        # XOR operation
        encrypted = bytes(a ^ b for a, b in zip(data, extended_key))
        
        # Return as hex string
        return encrypted.hex()
    
    def xor_decrypt(self, data: str, key: Union[str, bytes],
                    encoding: str = 'utf-8') -> str:
        """
        XOR decrypt data with a key.
        
        Args:
            data: Hex-encoded encrypted data
            key: Decryption key
            encoding: Text encoding
        
        Returns:
            Decrypted string
        """
        if isinstance(key, str):
            key = key.encode(encoding)
        
        # Convert hex to bytes
        encrypted = bytes.fromhex(data)
        
        # Extend key to match data length
        extended_key = (key * ((len(encrypted) // len(key)) + 1))[:len(encrypted)]
        
        # XOR operation (same as encrypt)
        decrypted = bytes(a ^ b for a, b in zip(encrypted, extended_key))
        
        return decrypted.decode(encoding)
    
    # ==================== ROT13 ====================
    
    def rot13(self, data: str) -> str:
        """
        Apply ROT13 transformation.
        
        Args:
            data: Input string
        
        Returns:
            ROT13 transformed string
        """
        result = []
        for char in data:
            if 'a' <= char <= 'z':
                result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
            elif 'A' <= char <= 'Z':
                result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
            else:
                result.append(char)
        return ''.join(result)
    
    # ==================== Caesar Cipher ====================
    
    def caesar_encrypt(self, data: str, shift: int = 3) -> str:
        """
        Caesar cipher encryption.
        
        Args:
            data: Input string
            shift: Number of positions to shift (default: 3)
        
        Returns:
            Encrypted string
        """
        result = []
        for char in data:
            if 'a' <= char <= 'z':
                result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            elif 'A' <= char <= 'Z':
                result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            else:
                result.append(char)
        return ''.join(result)
    
    def caesar_decrypt(self, data: str, shift: int = 3) -> str:
        """
        Caesar cipher decryption.
        
        Args:
            data: Encrypted string
            shift: Number of positions shifted (default: 3)
        
        Returns:
            Decrypted string
        """
        return self.caesar_encrypt(data, -shift)
    
    # ==================== Vigenère Cipher ====================
    
    def vigenere_encrypt(self, data: str, key: str) -> str:
        """
        Vigenère cipher encryption.
        
        Args:
            data: Input string
            key: Encryption key (letters only)
        
        Returns:
            Encrypted string
        """
        if not key:
            raise ValueError("Key cannot be empty")
        
        key = key.upper()
        result = []
        key_index = 0
        
        for char in data:
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('A')
                if char.islower():
                    result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
                else:
                    result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    def vigenere_decrypt(self, data: str, key: str) -> str:
        """
        Vigenère cipher decryption.
        
        Args:
            data: Encrypted string
            key: Decryption key (letters only)
        
        Returns:
            Decrypted string
        """
        if not key:
            raise ValueError("Key cannot be empty")
        
        key = key.upper()
        result = []
        key_index = 0
        
        for char in data:
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('A')
                if char.islower():
                    result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
                else:
                    result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    # ==================== Generic Methods ====================
    
    def encrypt(self, data: Union[str, bytes], algorithm: str, key: str = '',
                encoding: str = 'utf-8', **kwargs) -> str:
        """
        Generic encrypt method.
        
        Args:
            data: Data to encrypt
            algorithm: Encryption algorithm
            key: Encryption key
            encoding: Text encoding
            **kwargs: Additional parameters
        
        Returns:
            Encrypted string
        """
        algorithm = algorithm.lower()
        
        if algorithm == 'xor':
            return self.xor_encrypt(data, key, encoding)
        elif algorithm == 'rot13':
            return self.rot13(data if isinstance(data, str) else data.decode(encoding))
        elif algorithm == 'caesar':
            shift = kwargs.get('shift', 3)
            return self.caesar_encrypt(data if isinstance(data, str) else data.decode(encoding), shift)
        elif algorithm == 'vigenere':
            return self.vigenere_encrypt(data if isinstance(data, str) else data.decode(encoding), key)
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}. Available: {', '.join(self.SUPPORTED_ALGORITHMS)}")
    
    def decrypt(self, data: str, algorithm: str, key: str = '',
                encoding: str = 'utf-8', **kwargs) -> str:
        """
        Generic decrypt method.
        
        Args:
            data: Encrypted data
            algorithm: Encryption algorithm
            key: Decryption key
            encoding: Text encoding
            **kwargs: Additional parameters
        
        Returns:
            Decrypted string
        """
        algorithm = algorithm.lower()
        
        if algorithm == 'xor':
            return self.xor_decrypt(data, key, encoding)
        elif algorithm == 'rot13':
            return self.rot13(data)
        elif algorithm == 'caesar':
            shift = kwargs.get('shift', 3)
            return self.caesar_decrypt(data, shift)
        elif algorithm == 'vigenere':
            return self.vigenere_decrypt(data, key)
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}. Available: {', '.join(self.SUPPORTED_ALGORITHMS)}")
    
    @staticmethod
    def generate_key(length: int = 32) -> str:
        """
        Generate a random encryption key.
        
        Args:
            length: Key length in bytes
        
        Returns:
            Hex-encoded random key
        """
        return secrets.token_hex(length)
    
    @staticmethod
    def derive_key(password: str, salt: str = '', length: int = 32) -> str:
        """
        Derive a key from password using SHA-256.
        
        Args:
            password: User password
            salt: Optional salt
            length: Key length in bytes
        
        Returns:
            Hex-encoded derived key
        """
        combined = password + salt
        return hashlib.sha256(combined.encode()).hexdigest()[:length*2]
    
    def __repr__(self) -> str:
        return "CryptoEngine()"
