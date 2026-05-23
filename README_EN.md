<p align="center">
  <a href="README.md">简体中文</a> | 
  <a href="README_EN.md">English</a> | 
  <a href="README_TW.md">繁體中文</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Dependencies-0-brightgreen.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/Tests-22%20passed-success.svg" alt="Tests">
</p>

<h1 align="center">🔐 HashForge-Lite</h1>

<p align="center">
  <b>Lightweight Terminal Hash, Encoding & Encryption Toolkit</b><br>
  <sub>Zero Dependencies • 12 Hash Algorithms • 8 Encodings • 4 Ciphers • Password Generator • TUI Dashboard</sub>
</p>

---

## 🎉 Introduction

**HashForge-Lite** is a zero-dependency terminal encryption toolkit that provides one-stop hash calculation, encoding conversion, and encryption/decryption capabilities. All features are implemented using only Python standard library - no external dependencies required.

### 💡 Design Philosophy

In daily development, we often need to perform hash calculations, Base64 encoding, password generation, and other operations. Existing tools are either scattered in functionality or require installing numerous dependencies. HashForge-Lite was born to solve this pain point - **one command-line tool covering all common encryption and encoding needs**.

### ✨ Core Features

| Module | Support | Description |
|--------|---------|-------------|
| 🔢 **Hash Calculation** | MD5, SHA-1, SHA-256, SHA-512, SHA3, BLAKE2 | 12 algorithms, text & file support |
| 📝 **Encoding** | Base64, Base32, Hex, URL, ASCII, Binary | 8 encodings, bidirectional conversion |
| 🔒 **Encryption** | XOR, ROT13, Caesar, Vigenère | 4 classic cipher algorithms |
| 🔑 **Password Generation** | Random password, passphrase, PIN | Configurable rules, strength analysis |
| 🖥️ **TUI Interface** | Interactive terminal dashboard | Real-time preview, keyboard navigation |

### 🚀 Quick Start

#### Requirements
- Python 3.8 or higher
- No external dependencies required

#### Installation

```bash
# Method 1: Install from source
git clone https://github.com/gitstq/HashForge-Lite.git
cd HashForge-Lite
pip install -e .

# Method 2: Run directly
python -m hashforge.cli --help
```

#### Basic Usage

```bash
# Hash calculation
hashforge hash "Hello World"                    # SHA-256 (default)
hashforge hash "Hello World" -a md5             # MD5
hashforge hash "Hello World" --all              # All algorithms
hashforge hash-file myfile.txt                  # File hash

# Encoding
hashforge encode "Hello World" -t base64        # Base64 encode
hashforge decode "SGVsbG8gV29ybGQ=" -t base64   # Base64 decode
hashforge encode "Hello World" --all            # All encodings

# Encryption
hashforge encrypt "Secret" -k "mykey"           # XOR encrypt
hashforge decrypt "encrypted_hex" -k "mykey"    # XOR decrypt
hashforge encrypt "Secret" -k "key" -a rot13    # ROT13

# Password generation
hashforge password                              # 16-char random password
hashforge password -l 20 --no-symbols           # 20 chars, no symbols
hashforge passphrase                            # Passphrase
hashforge pin -l 6                              # 6-digit PIN
hashforge analyze "MyP@ssw0rd"                  # Password strength analysis

# TUI interface
hashforge tui                                   # Launch interactive UI
```

---

## 📖 Detailed Usage Guide

### Hash Calculation Module

Supports 12 hash algorithms:

```bash
# List all supported algorithms
hashforge list

# Text hash
hashforge hash "password123" -a sha256
# Output: ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f

# File hash
hashforge hash-file document.pdf -a sha512

# Verify hash
hashforge hash "test" --verify <expected_hash>
```

### Encoding Module

Supports 8 encoding formats:

```bash
# Base64
hashforge encode "Hello" -t base64
hashforge decode "SGVsbG8=" -t base64

# Hexadecimal
hashforge encode "Hello" -t hex
hashforge decode "48656c6c6f" -t hex

# URL encoding
hashforge encode "Hello World" -t url
hashforge decode "Hello%20World" -t url

# ASCII code
hashforge encode "ABC" -t ascii
# Output: 65 66 67

# Binary
hashforge encode "A" -t binary
# Output: 01000001
```

### Encryption Module

Supports 4 encryption algorithms:

```bash
# XOR encryption (recommended)
hashforge encrypt "Secret Message" -k "mykey" -a xor
hashforge decrypt "encrypted_hex" -k "mykey" -a xor

# ROT13 (self-inverse)
hashforge encrypt "Hello" -a rot13
# Output: Uryyb

# Caesar cipher
hashforge encrypt "ABC" -a caesar --shift 3
# Output: DEF

# Vigenère cipher
hashforge encrypt "HELLO" -k "KEY" -a vigenere
```

### Password Generation Module

```bash
# Generate strong password
hashforge password -l 24
# Output: Kx9#mP2$vL5@nQ8&wR3!

# Generate passphrase
hashforge passphrase -w 4 --capitalize --number
# Output: Mountain-River-42-Sunset

# Analyze password strength
hashforge analyze "MyStr0ng!Pass"
# Output: strength, entropy, suggestions, etc.

# Generate multiple passwords
hashforge password -c 5 -l 16
```

### TUI Interactive Interface

```bash
hashforge tui
```

Launches interactive terminal interface with:
- 🔄 Tab key to switch modules
- ⬅️➡️ Arrow keys to select algorithms
- ⌨️ Direct text input
- ↵ Enter to execute
- C to clear input
- Q to quit

---

## 💡 Design & Roadmap

### Technology Choices

| Choice | Reason |
|--------|--------|
| **Python Standard Library** | Zero dependencies, works out of the box, cross-platform |
| **argparse** | Built-in CLI framework, stable and reliable |
| **curses** | Terminal UI standard library, no extra installation |
| **hashlib/secrets** | Cryptographically secure, industry standard |

### Future Roadmap

- [ ] Add AES-256 encryption support
- [ ] Support batch file processing
- [ ] Add more hash algorithms (bcrypt, scrypt)
- [ ] Support configuration files
- [ ] Add more language support

---

## 📦 Build & Deploy

### Build Wheel Package

```bash
pip install wheel
python setup.py sdist bdist_wheel
```

### System Installation

```bash
pip install dist/hashforge-1.0.0-py3-none-any.whl
```

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

### Commit Convention

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `refactor:` Code refactoring
- `test:` Test related

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ by HashForge Team
</p>
