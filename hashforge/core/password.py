#!/usr/bin/env python3
"""
Password Generator Module - 密码生成模块
Generate secure random passwords with configurable rules.
"""

import secrets
import string
import re
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
from enum import Enum


class PasswordStrength(Enum):
    """Password strength levels."""
    VERY_WEAK = 1
    WEAK = 2
    MEDIUM = 3
    STRONG = 4
    VERY_STRONG = 5


@dataclass
class PasswordAnalysis:
    """Password analysis result."""
    password: str
    length: int
    strength: PasswordStrength
    score: int
    has_lowercase: bool
    has_uppercase: bool
    has_digits: bool
    has_symbols: bool
    entropy: float
    suggestions: List[str]


class PasswordGenerator:
    """
    Lightweight password generator with strength analysis.
    
    Features:
        - Generate random passwords with configurable rules
        - Password strength analysis
        - Entropy calculation
        - Passphrase generation
    """
    
    # Character sets
    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SYMBOLS = '!@#$%^&*()_+-=[]{}|;:,.<>?'
    AMBIGUOUS = 'l1IO0'
    
    # Common weak patterns
    WEAK_PATTERNS = [
        r'(.)\1{2,}',  # Repeated characters
        r'(012|123|234|345|456|567|678|789|890)',  # Sequential numbers
        r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)',  # Sequential letters
        r'(qwerty|asdfgh|zxcvbn)',  # Keyboard patterns
    ]
    
    def __init__(self):
        """Initialize password generator."""
        pass
    
    def generate(self, length: int = 16, 
                 lowercase: bool = True,
                 uppercase: bool = True,
                 digits: bool = True,
                 symbols: bool = True,
                 exclude_ambiguous: bool = False,
                 exclude: str = '') -> str:
        """
        Generate a random password.
        
        Args:
            length: Password length (default: 16)
            lowercase: Include lowercase letters
            uppercase: Include uppercase letters
            digits: Include digits
            symbols: Include symbols
            exclude_ambiguous: Exclude ambiguous characters (l, 1, I, O, 0)
            exclude: Characters to exclude
        
        Returns:
            Generated password
        
        Raises:
            ValueError: If no character sets are selected
        """
        if length < 4:
            raise ValueError("Password length must be at least 4")
        
        # Build character set
        charset = ''
        required = []
        
        if lowercase:
            chars = self.LOWERCASE
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.AMBIGUOUS)
            charset += chars
            required.append(secrets.choice(chars))
        
        if uppercase:
            chars = self.UPPERCASE
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.AMBIGUOUS)
            charset += chars
            required.append(secrets.choice(chars))
        
        if digits:
            chars = self.DIGITS
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.AMBIGUOUS)
            charset += chars
            required.append(secrets.choice(chars))
        
        if symbols:
            charset += self.SYMBOLS
            required.append(secrets.choice(self.SYMBOLS))
        
        if not charset:
            raise ValueError("At least one character set must be selected")
        
        # Exclude specified characters
        if exclude:
            charset = ''.join(c for c in charset if c not in exclude)
            if not charset:
                raise ValueError("No characters remaining after exclusions")
        
        # Generate password
        remaining_length = length - len(required)
        password_chars = required + [secrets.choice(charset) for _ in range(remaining_length)]
        
        # Shuffle using secrets
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def generate_passphrase(self, word_count: int = 4, 
                           separator: str = '-',
                           capitalize: bool = False,
                           include_number: bool = False) -> str:
        """
        Generate a passphrase from common words.
        
        Args:
            word_count: Number of words (default: 4)
            separator: Word separator (default: -)
            capitalize: Capitalize first letter of each word
            include_number: Include a random number
        
        Returns:
            Generated passphrase
        """
        # Built-in word list (common English words)
        words = [
            'apple', 'banana', 'cherry', 'dragon', 'elephant',
            'forest', 'garden', 'harbor', 'island', 'jungle',
            'kitchen', 'lemon', 'mountain', 'night', 'ocean',
            'planet', 'queen', 'river', 'sunset', 'tiger',
            'umbrella', 'valley', 'window', 'yellow', 'zebra',
            'bridge', 'castle', 'diamond', 'energy', 'flower',
            'guitar', 'horizon', 'insect', 'jacket', 'kingdom',
            'library', 'market', 'notebook', 'orange', 'piano',
            'quality', 'rainbow', 'silver', 'thunder', 'uniform',
            'village', 'wisdom', 'xylophone', 'yogurt', 'zephyr'
        ]
        
        selected = [secrets.choice(words) for _ in range(word_count)]
        
        if capitalize:
            selected = [w.capitalize() for w in selected]
        
        if include_number:
            # Insert a random number in a random position
            num = str(secrets.randbelow(100))
            pos = secrets.randbelow(len(selected))
            selected.insert(pos, num)
        
        return separator.join(selected)
    
    def generate_pin(self, length: int = 6) -> str:
        """
        Generate a numeric PIN.
        
        Args:
            length: PIN length (default: 6)
        
        Returns:
            Generated PIN
        """
        return ''.join(secrets.choice(string.digits) for _ in range(length))
    
    def analyze(self, password: str) -> PasswordAnalysis:
        """
        Analyze password strength.
        
        Args:
            password: Password to analyze
        
        Returns:
            PasswordAnalysis object
        """
        length = len(password)
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_symbol = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
        
        # Calculate score
        score = 0
        
        # Length score
        if length >= 8:
            score += 1
        if length >= 12:
            score += 1
        if length >= 16:
            score += 1
        if length >= 20:
            score += 1
        
        # Character variety score
        variety = sum([has_lower, has_upper, has_digit, has_symbol])
        score += variety
        
        # Check for weak patterns
        pattern_penalty = 0
        for pattern in self.WEAK_PATTERNS:
            if re.search(pattern, password.lower()):
                pattern_penalty += 1
        score -= pattern_penalty
        
        # Clamp score
        score = max(1, min(5, score))
        
        # Determine strength
        strength = PasswordStrength(score)
        
        # Calculate entropy
        charset_size = 0
        if has_lower:
            charset_size += 26
        if has_upper:
            charset_size += 26
        if has_digit:
            charset_size += 10
        if has_symbol:
            charset_size += 32
        
        import math
        entropy = length * math.log2(charset_size) if charset_size > 0 else 0
        
        # Generate suggestions
        suggestions = []
        if length < 12:
            suggestions.append("Use at least 12 characters")
        if not has_lower:
            suggestions.append("Add lowercase letters")
        if not has_upper:
            suggestions.append("Add uppercase letters")
        if not has_digit:
            suggestions.append("Add numbers")
        if not has_symbol:
            suggestions.append("Add special characters")
        if pattern_penalty > 0:
            suggestions.append("Avoid common patterns")
        
        return PasswordAnalysis(
            password=password,
            length=length,
            strength=strength,
            score=score,
            has_lowercase=has_lower,
            has_uppercase=has_upper,
            has_digits=has_digit,
            has_symbols=has_symbol,
            entropy=entropy,
            suggestions=suggestions
        )
    
    def check_strength(self, password: str) -> Tuple[str, int]:
        """
        Quick password strength check.
        
        Args:
            password: Password to check
        
        Returns:
            Tuple of (strength_name, score)
        """
        analysis = self.analyze(password)
        return (analysis.strength.name.replace('_', ' ').title(), analysis.score)
    
    def generate_multiple(self, count: int = 5, **kwargs) -> List[str]:
        """
        Generate multiple passwords.
        
        Args:
            count: Number of passwords to generate
            **kwargs: Arguments for generate()
        
        Returns:
            List of generated passwords
        """
        return [self.generate(**kwargs) for _ in range(count)]
    
    def __repr__(self) -> str:
        return "PasswordGenerator()"
