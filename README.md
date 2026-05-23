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
  <b>轻量级终端哈希、编码与加密工具集</b><br>
  <sub>Zero Dependencies • 12 Hash Algorithms • 8 Encodings • 4 Ciphers • Password Generator • TUI Dashboard</sub>
</p>

---

## 🎉 项目介绍

**HashForge-Lite** 是一款零依赖的终端加密工具集，为开发者提供一站式哈希计算、编码转换、加密解密功能。所有功能仅使用 Python 标准库实现，无需安装任何外部依赖。

### 💡 设计理念

在日常开发中，我们经常需要进行哈希计算、Base64 编码、密码生成等操作。现有工具要么功能分散，要么需要安装大量依赖。HashForge-Lite 的诞生就是为了解决这个痛点——**一个命令行工具，覆盖所有常见加密编码需求**。

### ✨ 核心特性

| 功能模块 | 支持项 | 说明 |
|---------|-------|------|
| 🔢 **哈希计算** | MD5, SHA-1, SHA-256, SHA-512, SHA3, BLAKE2 | 12 种算法，支持文本和文件 |
| 📝 **编码转换** | Base64, Base32, Hex, URL, ASCII, Binary | 8 种编码，双向转换 |
| 🔒 **加密解密** | XOR, ROT13, Caesar, Vigenère | 4 种经典密码算法 |
| 🔑 **密码生成** | 随机密码、密码短语、PIN码 | 可配置规则，强度分析 |
| 🖥️ **TUI 界面** | 交互式终端仪表盘 | 实时预览，键盘操作 |

### 🚀 快速开始

#### 环境要求
- Python 3.8 或更高版本
- 无需任何外部依赖

#### 安装方式

```bash
# 方式一：从源码安装
git clone https://github.com/gitstq/HashForge-Lite.git
cd HashForge-Lite
pip install -e .

# 方式二：直接运行
python -m hashforge.cli --help
```

#### 基础用法

```bash
# 哈希计算
hashforge hash "Hello World"                    # SHA-256 (默认)
hashforge hash "Hello World" -a md5             # MD5
hashforge hash "Hello World" --all              # 所有算法
hashforge hash-file myfile.txt                  # 文件哈希

# 编码转换
hashforge encode "Hello World" -t base64        # Base64 编码
hashforge decode "SGVsbG8gV29ybGQ=" -t base64   # Base64 解码
hashforge encode "Hello World" --all            # 所有编码

# 加密解密
hashforge encrypt "Secret" -k "mykey"           # XOR 加密
hashforge decrypt "encrypted_hex" -k "mykey"    # XOR 解密
hashforge encrypt "Secret" -k "key" -a rot13    # ROT13

# 密码生成
hashforge password                              # 16位随机密码
hashforge password -l 20 --no-symbols           # 20位，无符号
hashforge passphrase                            # 密码短语
hashforge pin -l 6                              # 6位PIN码
hashforge analyze "MyP@ssw0rd"                  # 密码强度分析

# TUI 界面
hashforge tui                                   # 启动交互界面
```

---

## 📖 详细使用指南

### 哈希计算模块

支持 12 种哈希算法：

```bash
# 查看所有支持的算法
hashforge list

# 文本哈希
hashforge hash "password123" -a sha256
# 输出: ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f

# 文件哈希
hashforge hash-file document.pdf -a sha512

# 验证哈希
hashforge hash "test" --verify <expected_hash>
```

### 编码转换模块

支持 8 种编码格式：

```bash
# Base64
hashforge encode "Hello" -t base64
hashforge decode "SGVsbG8=" -t base64

# 十六进制
hashforge encode "Hello" -t hex
hashforge decode "48656c6c6f" -t hex

# URL 编码
hashforge encode "Hello World" -t url
hashforge decode "Hello%20World" -t url

# ASCII 码
hashforge encode "ABC" -t ascii
# 输出: 65 66 67

# 二进制
hashforge encode "A" -t binary
# 输出: 01000001
```

### 加密解密模块

支持 4 种加密算法：

```bash
# XOR 加密（推荐）
hashforge encrypt "Secret Message" -k "mykey" -a xor
hashforge decrypt "encrypted_hex" -k "mykey" -a xor

# ROT13（自逆运算）
hashforge encrypt "Hello" -a rot13
# 输出: Uryyb

# Caesar 密码
hashforge encrypt "ABC" -a caesar --shift 3
# 输出: DEF

# Vigenère 密码
hashforge encrypt "HELLO" -k "KEY" -a vigenere
```

### 密码生成模块

```bash
# 生成强密码
hashforge password -l 24
# 输出: Kx9#mP2$vL5@nQ8&wR3!

# 生成密码短语
hashforge passphrase -w 4 --capitalize --number
# 输出: Mountain-River-42-Sunset

# 分析密码强度
hashforge analyze "MyStr0ng!Pass"
# 输出: 强度、熵值、建议等

# 生成多个密码
hashforge password -c 5 -l 16
```

### TUI 交互界面

```bash
hashforge tui
```

启动交互式终端界面，支持：
- 🔄 Tab 键切换功能模块
- ⬅️➡️ 方向键选择算法
- ⌨️ 直接输入文本
- ↵ Enter 执行操作
- C 清空输入
- Q 退出程序

---

## 💡 设计思路与迭代规划

### 技术选型

| 选择 | 原因 |
|-----|------|
| **Python 标准库** | 零依赖，开箱即用，跨平台兼容 |
| **argparse** | Python 内置 CLI 框架，稳定可靠 |
| **curses** | 终端 UI 标准库，无需额外安装 |
| **hashlib/secrets** | 加密安全，符合行业标准 |

### 后续迭代计划

- [ ] 添加 AES-256 加密支持
- [ ] 支持批量文件处理
- [ ] 添加更多哈希算法（如 bcrypt、scrypt）
- [ ] 支持配置文件
- [ ] 添加更多语言支持

---

## 📦 打包与部署

### 构建 Wheel 包

```bash
pip install wheel
python setup.py sdist bdist_wheel
```

### 安装到系统

```bash
pip install dist/hashforge-1.0.0-py3-none-any.whl
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 提交规范

- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

<p align="center">
  Made with ❤️ by HashForge Team
</p>
