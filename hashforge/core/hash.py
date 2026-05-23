#!/usr/bin/env python3
"""
Hash Calculator Module - 哈希计算模块
Supports MD5, SHA-1, SHA-256, SHA-512 and more.
"""

import hashlib
from typing import Union, Optional, Dict, List
from pathlib import Path


class HashCalculator:
    """
    Lightweight hash calculator supporting multiple algorithms.
    
    Supported algorithms:
        - MD5
        - SHA-1
        - SHA-224
        - SHA-256
        - SHA-384
        - SHA-512
        - SHA3-224
        - SHA3-256
        - SHA3-384
        - SHA3-512
        - BLAKE2b
        - BLAKE2s
    """
    
    SUPPORTED_ALGORITHMS = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha224': hashlib.sha224,
        'sha256': hashlib.sha256,
        'sha384': hashlib.sha384,
        'sha512': hashlib.sha512,
        'sha3-224': hashlib.sha3_224,
        'sha3-256': hashlib.sha3_256,
        'sha3-384': hashlib.sha3_384,
        'sha3-512': hashlib.sha3_512,
        'blake2b': hashlib.blake2b,
        'blake2s': hashlib.blake2s,
    }
    
    def __init__(self, algorithm: str = 'sha256'):
        """
        Initialize hash calculator with specified algorithm.
        
        Args:
            algorithm: Hash algorithm name (default: sha256)
        
        Raises:
            ValueError: If algorithm is not supported
        """
        algorithm_lower = algorithm.lower().replace('_', '-')
        if algorithm_lower not in self.SUPPORTED_ALGORITHMS:
            available = ', '.join(self.SUPPORTED_ALGORITHMS.keys())
            raise ValueError(f"Unsupported algorithm: {algorithm}. Available: {available}")
        self.algorithm = algorithm_lower
        self._hash_func = self.SUPPORTED_ALGORITHMS[algorithm_lower]
    
    def hash_string(self, text: str, encoding: str = 'utf-8') -> str:
        """
        Calculate hash of a string.
        
        Args:
            text: Input string
            encoding: Text encoding (default: utf-8)
        
        Returns:
            Hexadecimal hash string
        """
        return self._hash_func(text.encode(encoding)).hexdigest()
    
    def hash_bytes(self, data: bytes) -> str:
        """
        Calculate hash of bytes.
        
        Args:
            data: Input bytes
        
        Returns:
            Hexadecimal hash string
        """
        return self._hash_func(data).hexdigest()
    
    def hash_file(self, file_path: Union[str, Path], chunk_size: int = 8192) -> str:
        """
        Calculate hash of a file.
        
        Args:
            file_path: Path to the file
            chunk_size: Size of chunks for reading large files
        
        Returns:
            Hexadecimal hash string
        
        Raises:
            FileNotFoundError: If file does not exist
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        hasher = self._hash_func()
        with open(path, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def hash_all(self, text: str, encoding: str = 'utf-8') -> Dict[str, str]:
        """
        Calculate all supported hashes for a string.
        
        Args:
            text: Input string
            encoding: Text encoding
        
        Returns:
            Dictionary mapping algorithm names to hash values
        """
        data = text.encode(encoding)
        return {algo: func(data).hexdigest() for algo, func in self.SUPPORTED_ALGORITHMS.items()}
    
    def hash_file_all(self, file_path: Union[str, Path], chunk_size: int = 8192) -> Dict[str, str]:
        """
        Calculate all supported hashes for a file.
        
        Args:
            file_path: Path to the file
            chunk_size: Size of chunks for reading large files
        
        Returns:
            Dictionary mapping algorithm names to hash values
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        hashers = {algo: func() for algo, func in self.SUPPORTED_ALGORITHMS.items()}
        
        with open(path, 'rb') as f:
            while chunk := f.read(chunk_size):
                for hasher in hashers.values():
                    hasher.update(chunk)
        
        return {algo: hasher.hexdigest() for algo, hasher in hashers.items()}
    
    def verify_hash(self, text: str, expected_hash: str, encoding: str = 'utf-8') -> bool:
        """
        Verify if a string matches an expected hash.
        
        Args:
            text: Input string
            expected_hash: Expected hash value
            encoding: Text encoding
        
        Returns:
            True if hash matches, False otherwise
        """
        actual_hash = self.hash_string(text, encoding)
        return actual_hash.lower() == expected_hash.lower()
    
    def verify_file_hash(self, file_path: Union[str, Path], expected_hash: str) -> bool:
        """
        Verify if a file matches an expected hash.
        
        Args:
            file_path: Path to the file
            expected_hash: Expected hash value
        
        Returns:
            True if hash matches, False otherwise
        """
        actual_hash = self.hash_file(file_path)
        return actual_hash.lower() == expected_hash.lower()
    
    @classmethod
    def list_algorithms(cls) -> List[str]:
        """
        List all supported hash algorithms.
        
        Returns:
            List of algorithm names
        """
        return list(cls.SUPPORTED_ALGORITHMS.keys())
    
    def __repr__(self) -> str:
        return f"HashCalculator(algorithm='{self.algorithm}')"
