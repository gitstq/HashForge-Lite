#!/usr/bin/env python3
"""
HashForge - Lightweight Terminal Hash, Encoding & Encryption Toolkit
轻量级终端哈希、编码与加密工具集

A zero-dependency CLI tool for hash calculation, encoding/decoding, and encryption.
"""

__version__ = "1.0.0"
__author__ = "HashForge Team"
__description__ = "Lightweight Terminal Hash, Encoding & Encryption Toolkit"

from .core.hash import HashCalculator
from .core.encode import Encoder
from .core.crypto import CryptoEngine
from .core.password import PasswordGenerator

__all__ = [
    "HashCalculator",
    "Encoder", 
    "CryptoEngine",
    "PasswordGenerator",
    "__version__",
]
