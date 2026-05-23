#!/usr/bin/env python3
"""
Encoder Module - 编码转换模块
Supports Base64, Base32, URL encoding, Hex, and more.
"""

import base64
import urllib.parse
import binascii
from typing import Union, Dict, Tuple, Optional
from pathlib import Path


class Encoder:
    """
    Lightweight encoder/decoder supporting multiple formats.
    
    Supported encodings:
        - Base64
        - Base32
        - Base16 (Hex)
        - URL encoding
        - Hexadecimal
        - ASCII
        - Binary
    """
    
    SUPPORTED_ENCODINGS = [
        'base64', 'base32', 'base16', 'hex',
        'url', 'ascii', 'binary'
    ]
    
    # ==================== Base64 ====================
    
    def base64_encode(self, data: Union[str, bytes], encoding: str = 'utf-8') -> str:
        """Encode string or bytes to Base64."""
        if isinstance(data, str):
            data = data.encode(encoding)
        return base64.b64encode(data).decode('ascii')
    
    def base64_decode(self, data: str, encoding: str = 'utf-8') -> str:
        """Decode Base64 string."""
        try:
            decoded = base64.b64decode(data)
            return decoded.decode(encoding)
        except Exception as e:
            raise ValueError(f"Base64 decode error: {e}")
    
    def base64url_encode(self, data: Union[str, bytes], encoding: str = 'utf-8') -> str:
        """Encode to URL-safe Base64."""
        if isinstance(data, str):
            data = data.encode(encoding)
        return base64.urlsafe_b64encode(data).decode('ascii')
    
    def base64url_decode(self, data: str, encoding: str = 'utf-8') -> str:
        """Decode URL-safe Base64 string."""
        try:
            decoded = base64.urlsafe_b64decode(data)
            return decoded.decode(encoding)
        except Exception as e:
            raise ValueError(f"Base64URL decode error: {e}")
    
    # ==================== Base32 ====================
    
    def base32_encode(self, data: Union[str, bytes], encoding: str = 'utf-8') -> str:
        """Encode string or bytes to Base32."""
        if isinstance(data, str):
            data = data.encode(encoding)
        return base64.b32encode(data).decode('ascii')
    
    def base32_decode(self, data: str, encoding: str = 'utf-8') -> str:
        """Decode Base32 string."""
        try:
            decoded = base64.b32decode(data)
            return decoded.decode(encoding)
        except Exception as e:
            raise ValueError(f"Base32 decode error: {e}")
    
    # ==================== Hex ====================
    
    def hex_encode(self, data: Union[str, bytes], encoding: str = 'utf-8') -> str:
        """Encode string or bytes to hexadecimal."""
        if isinstance(data, str):
            data = data.encode(encoding)
        return binascii.hexlify(data).decode('ascii')
    
    def hex_decode(self, data: str, encoding: str = 'utf-8') -> str:
        """Decode hexadecimal string."""
        try:
            decoded = binascii.unhexlify(data)
            return decoded.decode(encoding)
        except Exception as e:
            raise ValueError(f"Hex decode error: {e}")
    
    # ==================== URL Encoding ====================
    
    def url_encode(self, data: str, encoding: str = 'utf-8') -> str:
        """URL encode a string."""
        return urllib.parse.quote(data, encoding=encoding)
    
    def url_decode(self, data: str, encoding: str = 'utf-8') -> str:
        """URL decode a string."""
        try:
            return urllib.parse.unquote(data, encoding=encoding)
        except Exception as e:
            raise ValueError(f"URL decode error: {e}")
    
    def url_encode_component(self, data: str, encoding: str = 'utf-8') -> str:
        """URL encode with full encoding (like encodeURIComponent)."""
        return urllib.parse.quote(data, safe='', encoding=encoding)
    
    # ==================== ASCII ====================
    
    def ascii_encode(self, data: str) -> str:
        """Convert string to ASCII codes (space-separated)."""
        return ' '.join(str(ord(c)) for c in data)
    
    def ascii_decode(self, data: str) -> str:
        """Convert ASCII codes to string."""
        try:
            codes = [int(c) for c in data.split()]
            return ''.join(chr(c) for c in codes)
        except Exception as e:
            raise ValueError(f"ASCII decode error: {e}")
    
    # ==================== Binary ====================
    
    def binary_encode(self, data: Union[str, bytes], encoding: str = 'utf-8') -> str:
        """Convert string or bytes to binary representation."""
        if isinstance(data, str):
            data = data.encode(encoding)
        return ' '.join(format(b, '08b') for b in data)
    
    def binary_decode(self, data: str, encoding: str = 'utf-8') -> str:
        """Convert binary representation to string."""
        try:
            binary_values = data.split()
            bytes_data = bytes(int(b, 2) for b in binary_values)
            return bytes_data.decode(encoding)
        except Exception as e:
            raise ValueError(f"Binary decode error: {e}")
    
    # ==================== Generic Methods ====================
    
    def encode(self, data: Union[str, bytes], encoding_type: str, 
               text_encoding: str = 'utf-8') -> str:
        """
        Generic encode method.
        
        Args:
            data: Input data
            encoding_type: Type of encoding (base64, base32, hex, url, ascii, binary)
            text_encoding: Text encoding for string conversion
        
        Returns:
            Encoded string
        """
        encoding_type = encoding_type.lower().replace('-', '')
        
        if encoding_type == 'base64':
            return self.base64_encode(data, text_encoding)
        elif encoding_type == 'base64url':
            return self.base64url_encode(data, text_encoding)
        elif encoding_type == 'base32':
            return self.base32_encode(data, text_encoding)
        elif encoding_type in ('hex', 'base16'):
            return self.hex_encode(data, text_encoding)
        elif encoding_type == 'url':
            return self.url_encode(data, text_encoding) if isinstance(data, str) else self.url_encode(data.decode(text_encoding), text_encoding)
        elif encoding_type == 'ascii':
            return self.ascii_encode(data) if isinstance(data, str) else self.ascii_encode(data.decode(text_encoding))
        elif encoding_type == 'binary':
            return self.binary_encode(data, text_encoding)
        else:
            raise ValueError(f"Unsupported encoding: {encoding_type}. Available: {', '.join(self.SUPPORTED_ENCODINGS)}")
    
    def decode(self, data: str, encoding_type: str, 
               text_encoding: str = 'utf-8') -> str:
        """
        Generic decode method.
        
        Args:
            data: Encoded string
            encoding_type: Type of encoding
            text_encoding: Text encoding for output
        
        Returns:
            Decoded string
        """
        encoding_type = encoding_type.lower().replace('-', '')
        
        if encoding_type == 'base64':
            return self.base64_decode(data, text_encoding)
        elif encoding_type == 'base64url':
            return self.base64url_decode(data, text_encoding)
        elif encoding_type == 'base32':
            return self.base32_decode(data, text_encoding)
        elif encoding_type in ('hex', 'base16'):
            return self.hex_decode(data, text_encoding)
        elif encoding_type == 'url':
            return self.url_decode(data, text_encoding)
        elif encoding_type == 'ascii':
            return self.ascii_decode(data)
        elif encoding_type == 'binary':
            return self.binary_decode(data, text_encoding)
        else:
            raise ValueError(f"Unsupported encoding: {encoding_type}. Available: {', '.join(self.SUPPORTED_ENCODINGS)}")
    
    def encode_all(self, data: str, encoding: str = 'utf-8') -> Dict[str, str]:
        """
        Encode string using all supported encodings.
        
        Args:
            data: Input string
            encoding: Text encoding
        
        Returns:
            Dictionary mapping encoding names to encoded values
        """
        return {
            'base64': self.base64_encode(data, encoding),
            'base64url': self.base64url_encode(data, encoding),
            'base32': self.base32_encode(data, encoding),
            'hex': self.hex_encode(data, encoding),
            'url': self.url_encode(data, encoding),
            'url_full': self.url_encode_component(data, encoding),
            'ascii': self.ascii_encode(data),
            'binary': self.binary_encode(data, encoding),
        }
    
    def detect_encoding(self, data: str) -> Dict[str, float]:
        """
        Attempt to detect the encoding of a string.
        
        Args:
            data: Encoded string
        
        Returns:
            Dictionary mapping encoding names to confidence scores
        """
        results = {}
        
        # Try Base64
        try:
            self.base64_decode(data)
            # Base64 strings have specific patterns
            import re
            if re.match(r'^[A-Za-z0-9+/]+=*$', data) and len(data) % 4 == 0:
                results['base64'] = 0.9
            else:
                results['base64'] = 0.5
        except:
            results['base64'] = 0.0
        
        # Try Base32
        try:
            self.base32_decode(data)
            import re
            if re.match(r'^[A-Z2-7]+=*$', data.upper()) and len(data) % 8 == 0:
                results['base32'] = 0.9
            else:
                results['base32'] = 0.5
        except:
            results['base32'] = 0.0
        
        # Try Hex
        try:
            self.hex_decode(data)
            import re
            if re.match(r'^[0-9a-fA-F]+$', data) and len(data) % 2 == 0:
                results['hex'] = 0.9
            else:
                results['hex'] = 0.5
        except:
            results['hex'] = 0.0
        
        # Try URL
        try:
            decoded = self.url_decode(data)
            if decoded != data and '%' in data:
                results['url'] = 0.8
            else:
                results['url'] = 0.3
        except:
            results['url'] = 0.0
        
        return results
    
    def __repr__(self) -> str:
        return "Encoder()"
