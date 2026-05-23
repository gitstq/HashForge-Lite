#!/usr/bin/env python3
"""
HashForge CLI - Command Line Interface
轻量级终端哈希、编码与加密工具集

Usage:
    hashforge hash <text> [--algorithm ALGO]
    hashforge hash-file <file> [--algorithm ALGO]
    hashforge encode <text> [--type TYPE]
    hashforge decode <text> [--type TYPE]
    hashforge encrypt <text> --key KEY [--algorithm ALGO]
    hashforge decrypt <text> --key KEY [--algorithm ALGO]
    hashforge password [--length N] [--no-symbols]
    hashforge analyze <password>
    hashforge tui
"""

import sys
import argparse
import json
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from hashforge.core import HashCalculator, Encoder, CryptoEngine, PasswordGenerator
from hashforge import __version__


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog='hashforge',
        description='🔐 HashForge - Lightweight Terminal Hash, Encoding & Encryption Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Hash operations
  hashforge hash "Hello World"                    # SHA-256 hash
  hashforge hash "Hello World" -a md5             # MD5 hash
  hashforge hash "Hello World" --all              # All hash algorithms
  hashforge hash-file myfile.txt                  # Hash a file
  
  # Encoding operations
  hashforge encode "Hello World" -t base64        # Base64 encode
  hashforge decode "SGVsbG8gV29ybGQ=" -t base64   # Base64 decode
  hashforge encode "Hello World" --all            # All encodings
  
  # Encryption operations
  hashforge encrypt "Secret" -k "mykey"           # XOR encrypt
  hashforge decrypt "encrypted_hex" -k "mykey"    # XOR decrypt
  hashforge encrypt "Secret" -k "key" -a rot13    # ROT13
  
  # Password operations
  hashforge password                               # Generate password
  hashforge password -l 20 --no-symbols           # 20 chars, no symbols
  hashforge passphrase                            # Generate passphrase
  hashforge analyze "MyP@ssw0rd"                  # Analyze password
        """
    )
    
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Hash command
    hash_parser = subparsers.add_parser('hash', help='Calculate hash of text')
    hash_parser.add_argument('text', help='Text to hash')
    hash_parser.add_argument('-a', '--algorithm', default='sha256',
                            choices=HashCalculator.list_algorithms(),
                            help='Hash algorithm (default: sha256)')
    hash_parser.add_argument('--all', action='store_true', help='Calculate all hashes')
    hash_parser.add_argument('-f', '--format', choices=['text', 'json'], default='text',
                            help='Output format')
    
    # Hash-file command
    hashfile_parser = subparsers.add_parser('hash-file', help='Calculate hash of file')
    hashfile_parser.add_argument('file', help='File path')
    hashfile_parser.add_argument('-a', '--algorithm', default='sha256',
                                 choices=HashCalculator.list_algorithms(),
                                 help='Hash algorithm (default: sha256)')
    hashfile_parser.add_argument('--all', action='store_true', help='Calculate all hashes')
    hashfile_parser.add_argument('-f', '--format', choices=['text', 'json'], default='text',
                                 help='Output format')
    
    # Encode command
    encode_parser = subparsers.add_parser('encode', help='Encode text')
    encode_parser.add_argument('text', help='Text to encode')
    encode_parser.add_argument('-t', '--type', default='base64',
                               choices=['base64', 'base64url', 'base32', 'hex', 'url', 'ascii', 'binary'],
                               help='Encoding type (default: base64)')
    encode_parser.add_argument('--all', action='store_true', help='Encode with all methods')
    encode_parser.add_argument('-f', '--format', choices=['text', 'json'], default='text',
                               help='Output format')
    
    # Decode command
    decode_parser = subparsers.add_parser('decode', help='Decode text')
    decode_parser.add_argument('text', help='Text to decode')
    decode_parser.add_argument('-t', '--type', default='base64',
                               choices=['base64', 'base64url', 'base32', 'hex', 'url', 'ascii', 'binary'],
                               help='Encoding type (default: base64)')
    
    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt text')
    encrypt_parser.add_argument('text', help='Text to encrypt')
    encrypt_parser.add_argument('-k', '--key', required=True, help='Encryption key')
    encrypt_parser.add_argument('-a', '--algorithm', default='xor',
                                choices=['xor', 'rot13', 'caesar', 'vigenere'],
                                help='Encryption algorithm (default: xor)')
    encrypt_parser.add_argument('--shift', type=int, default=3, help='Caesar shift value')
    
    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt text')
    decrypt_parser.add_argument('text', help='Text to decrypt')
    decrypt_parser.add_argument('-k', '--key', required=True, help='Decryption key')
    decrypt_parser.add_argument('-a', '--algorithm', default='xor',
                                choices=['xor', 'rot13', 'caesar', 'vigenere'],
                                help='Decryption algorithm (default: xor)')
    decrypt_parser.add_argument('--shift', type=int, default=3, help='Caesar shift value')
    
    # Password command
    pwd_parser = subparsers.add_parser('password', help='Generate random password')
    pwd_parser.add_argument('-l', '--length', type=int, default=16, help='Password length')
    pwd_parser.add_argument('--no-lowercase', action='store_true', help='Exclude lowercase')
    pwd_parser.add_argument('--no-uppercase', action='store_true', help='Exclude uppercase')
    pwd_parser.add_argument('--no-digits', action='store_true', help='Exclude digits')
    pwd_parser.add_argument('--no-symbols', action='store_true', help='Exclude symbols')
    pwd_parser.add_argument('--exclude-ambiguous', action='store_true', help='Exclude ambiguous chars')
    pwd_parser.add_argument('-c', '--count', type=int, default=1, help='Number of passwords')
    
    # Passphrase command
    pp_parser = subparsers.add_parser('passphrase', help='Generate passphrase')
    pp_parser.add_argument('-w', '--words', type=int, default=4, help='Number of words')
    pp_parser.add_argument('-s', '--separator', default='-', help='Word separator')
    pp_parser.add_argument('--capitalize', action='store_true', help='Capitalize words')
    pp_parser.add_argument('--number', action='store_true', help='Include random number')
    
    # PIN command
    pin_parser = subparsers.add_parser('pin', help='Generate numeric PIN')
    pin_parser.add_argument('-l', '--length', type=int, default=6, help='PIN length')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze password strength')
    analyze_parser.add_argument('password', help='Password to analyze')
    
    # TUI command
    subparsers.add_parser('tui', help='Launch interactive TUI dashboard')
    
    # List command
    subparsers.add_parser('list', help='List supported algorithms')
    
    return parser


def cmd_hash(args):
    """Handle hash command."""
    calc = HashCalculator(args.algorithm)
    
    if args.all:
        result = calc.hash_all(args.text)
        if args.format == 'json':
            print(json.dumps(result, indent=2))
        else:
            for algo, hash_val in result.items():
                print(f"{algo.upper():12} {hash_val}")
    else:
        result = calc.hash_string(args.text)
        if args.format == 'json':
            print(json.dumps({args.algorithm: result}, indent=2))
        else:
            print(result)


def cmd_hash_file(args):
    """Handle hash-file command."""
    path = Path(args.file)
    if not path.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    
    calc = HashCalculator(args.algorithm)
    
    if args.all:
        result = calc.hash_file_all(path)
        if args.format == 'json':
            print(json.dumps(result, indent=2))
        else:
            print(f"File: {path}")
            for algo, hash_val in result.items():
                print(f"{algo.upper():12} {hash_val}")
    else:
        result = calc.hash_file(path)
        if args.format == 'json':
            print(json.dumps({args.algorithm: result, 'file': str(path)}, indent=2))
        else:
            print(f"{args.algorithm.upper()}  {path}")
            print(result)


def cmd_encode(args):
    """Handle encode command."""
    encoder = Encoder()
    
    if args.all:
        result = encoder.encode_all(args.text)
        if args.format == 'json':
            print(json.dumps(result, indent=2))
        else:
            for enc_type, value in result.items():
                print(f"{enc_type.upper():12} {value[:80]}{'...' if len(value) > 80 else ''}")
    else:
        result = encoder.encode(args.text, args.type)
        if args.format == 'json':
            print(json.dumps({args.type: result}, indent=2))
        else:
            print(result)


def cmd_decode(args):
    """Handle decode command."""
    encoder = Encoder()
    try:
        result = encoder.decode(args.text, args.type)
        print(result)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_encrypt(args):
    """Handle encrypt command."""
    crypto = CryptoEngine()
    kwargs = {}
    if args.algorithm == 'caesar':
        kwargs['shift'] = args.shift
    
    result = crypto.encrypt(args.text, args.algorithm, args.key, **kwargs)
    print(result)


def cmd_decrypt(args):
    """Handle decrypt command."""
    crypto = CryptoEngine()
    kwargs = {}
    if args.algorithm == 'caesar':
        kwargs['shift'] = args.shift
    
    result = crypto.decrypt(args.text, args.algorithm, args.key, **kwargs)
    print(result)


def cmd_password(args):
    """Handle password command."""
    gen = PasswordGenerator()
    
    for _ in range(args.count):
        pwd = gen.generate(
            length=args.length,
            lowercase=not args.no_lowercase,
            uppercase=not args.no_uppercase,
            digits=not args.no_digits,
            symbols=not args.no_symbols,
            exclude_ambiguous=args.exclude_ambiguous
        )
        print(pwd)


def cmd_passphrase(args):
    """Handle passphrase command."""
    gen = PasswordGenerator()
    pwd = gen.generate_passphrase(
        word_count=args.words,
        separator=args.separator,
        capitalize=args.capitalize,
        include_number=args.number
    )
    print(pwd)


def cmd_pin(args):
    """Handle pin command."""
    gen = PasswordGenerator()
    print(gen.generate_pin(args.length))


def cmd_analyze(args):
    """Handle analyze command."""
    gen = PasswordGenerator()
    analysis = gen.analyze(args.password)
    
    print(f"\n📊 Password Analysis")
    print(f"{'='*40}")
    print(f"Password:    {'*' * len(args.password)}")
    print(f"Length:      {analysis.length}")
    print(f"Strength:    {analysis.strength.name.replace('_', ' ').title()}")
    print(f"Score:       {analysis.score}/5")
    print(f"Entropy:     {analysis.entropy:.1f} bits")
    print(f"\nCharacter Types:")
    print(f"  Lowercase: {'✓' if analysis.has_lowercase else '✗'}")
    print(f"  Uppercase: {'✓' if analysis.has_uppercase else '✗'}")
    print(f"  Digits:    {'✓' if analysis.has_digits else '✗'}")
    print(f"  Symbols:   {'✓' if analysis.has_symbols else '✗'}")
    
    if analysis.suggestions:
        print(f"\n💡 Suggestions:")
        for s in analysis.suggestions:
            print(f"  • {s}")


def cmd_list(args):
    """Handle list command."""
    print("\n🔐 Supported Hash Algorithms:")
    print("   " + ", ".join(HashCalculator.list_algorithms()))
    
    print("\n📝 Supported Encodings:")
    print("   " + ", ".join(Encoder.SUPPORTED_ENCODINGS))
    
    print("\n🔒 Supported Encryption:")
    print("   " + ", ".join(CryptoEngine.SUPPORTED_ALGORITHMS))


def cmd_tui(args):
    """Handle TUI command."""
    try:
        from hashforge.tui.dashboard import run_tui
        run_tui()
    except ImportError:
        print("TUI module not available. Install with: pip install hashforge[tui]")
        sys.exit(1)


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Route to command handlers
    commands = {
        'hash': cmd_hash,
        'hash-file': cmd_hash_file,
        'encode': cmd_encode,
        'decode': cmd_decode,
        'encrypt': cmd_encrypt,
        'decrypt': cmd_decrypt,
        'password': cmd_password,
        'passphrase': cmd_passphrase,
        'pin': cmd_pin,
        'analyze': cmd_analyze,
        'list': cmd_list,
        'tui': cmd_tui,
    }
    
    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
