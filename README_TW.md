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
  <b>輕量級終端機雜湊、編碼與加密工具集</b><br>
  <sub>零依賴 • 12 種雜湊演算法 • 8 種編碼 • 4 種密碼 • 密碼產生器 • TUI 儀表板</sub>
</p>

---

## 🎉 專案介紹

**HashForge-Lite** 是一款零依賴的終端機加密工具集，為開發者提供一站式雜湊計算、編碼轉換、加密解密功能。所有功能僅使用 Python 標準函式庫實作，無需安裝任何外部依賴。

### 💡 設計理念

在日常開發中，我們經常需要進行雜湊計算、Base64 編碼、密碼產生等操作。現有工具要麼功能分散，要麼需要安裝大量依賴。HashForge-Lite 的誕生就是為了解決這個痛點——**一個命令列工具，涵蓋所有常見加密編碼需求**。

### ✨ 核心特性

| 功能模組 | 支援項目 | 說明 |
|---------|---------|------|
| 🔢 **雜湊計算** | MD5, SHA-1, SHA-256, SHA-512, SHA3, BLAKE2 | 12 種演算法，支援文字和檔案 |
| 📝 **編碼轉換** | Base64, Base32, Hex, URL, ASCII, Binary | 8 種編碼，雙向轉換 |
| 🔒 **加密解密** | XOR, ROT13, Caesar, Vigenère | 4 種經典密碼演算法 |
| 🔑 **密碼產生** | 隨機密碼、密碼短語、PIN碼 | 可設定規則，強度分析 |
| 🖥️ **TUI 介面** | 互動式終端機儀表板 | 即時預覽，鍵盤操作 |

### 🚀 快速開始

#### 環境需求
- Python 3.8 或更高版本
- 無需任何外部依賴

#### 安裝方式

```bash
# 方式一：從原始碼安裝
git clone https://github.com/gitstq/HashForge-Lite.git
cd HashForge-Lite
pip install -e .

# 方式二：直接執行
python -m hashforge.cli --help
```

#### 基礎用法

```bash
# 雜湊計算
hashforge hash "Hello World"                    # SHA-256 (預設)
hashforge hash "Hello World" -a md5             # MD5
hashforge hash "Hello World" --all              # 所有演算法
hashforge hash-file myfile.txt                  # 檔案雜湊

# 編碼轉換
hashforge encode "Hello World" -t base64        # Base64 編碼
hashforge decode "SGVsbG8gV29ybGQ=" -t base64   # Base64 解碼
hashforge encode "Hello World" --all            # 所有編碼

# 加密解密
hashforge encrypt "Secret" -k "mykey"           # XOR 加密
hashforge decrypt "encrypted_hex" -k "mykey"    # XOR 解密
hashforge encrypt "Secret" -k "key" -a rot13    # ROT13

# 密碼產生
hashforge password                              # 16位隨機密碼
hashforge password -l 20 --no-symbols           # 20位，無符號
hashforge passphrase                            # 密碼短語
hashforge pin -l 6                              # 6位PIN碼
hashforge analyze "MyP@ssw0rd"                  # 密碼強度分析

# TUI 介面
hashforge tui                                   # 啟動互動介面
```

---

## 📖 詳細使用指南

### 雜湊計算模組

支援 12 種雜湊演算法：

```bash
# 查看所有支援的演算法
hashforge list

# 文字雜湊
hashforge hash "password123" -a sha256
# 輸出: ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f

# 檔案雜湊
hashforge hash-file document.pdf -a sha512

# 驗證雜湊
hashforge hash "test" --verify <expected_hash>
```

### 編碼轉換模組

支援 8 種編碼格式：

```bash
# Base64
hashforge encode "Hello" -t base64
hashforge decode "SGVsbG8=" -t base64

# 十六進位
hashforge encode "Hello" -t hex
hashforge decode "48656c6c6f" -t hex

# URL 編碼
hashforge encode "Hello World" -t url
hashforge decode "Hello%20World" -t url

# ASCII 碼
hashforge encode "ABC" -t ascii
# 輸出: 65 66 67

# 二進位
hashforge encode "A" -t binary
# 輸出: 01000001
```

### 加密解密模組

支援 4 種加密演算法：

```bash
# XOR 加密（推薦）
hashforge encrypt "Secret Message" -k "mykey" -a xor
hashforge decrypt "encrypted_hex" -k "mykey" -a xor

# ROT13（自逆運算）
hashforge encrypt "Hello" -a rot13
# 輸出: Uryyb

# Caesar 密碼
hashforge encrypt "ABC" -a caesar --shift 3
# 輸出: DEF

# Vigenère 密碼
hashforge encrypt "HELLO" -k "KEY" -a vigenere
```

### 密碼產生模組

```bash
# 產生強密碼
hashforge password -l 24
# 輸出: Kx9#mP2$vL5@nQ8&wR3!

# 產生密碼短語
hashforge passphrase -w 4 --capitalize --number
# 輸出: Mountain-River-42-Sunset

# 分析密碼強度
hashforge analyze "MyStr0ng!Pass"
# 輸出: 強度、熵值、建議等

# 產生多個密碼
hashforge password -c 5 -l 16
```

### TUI 互動介面

```bash
hashforge tui
```

啟動互動式終端機介面，支援：
- 🔄 Tab 鍵切換功能模組
- ⬅️➡️ 方向鍵選擇演算法
- ⌨️ 直接輸入文字
- ↵ Enter 執行操作
- C 清空輸入
- Q 離開程式

---

## 💡 設計思路與迭代規劃

### 技術選型

| 選擇 | 原因 |
|-----|------|
| **Python 標準函式庫** | 零依賴，開箱即用，跨平台相容 |
| **argparse** | Python 內建 CLI 框架，穩定可靠 |
| **curses** | 終端機 UI 標準函式庫，無需額外安裝 |
| **hashlib/secrets** | 加密安全，符合業界標準 |

### 後續迭代計畫

- [ ] 新增 AES-256 加密支援
- [ ] 支援批次檔案處理
- [ ] 新增更多雜湊演算法（如 bcrypt、scrypt）
- [ ] 支援設定檔
- [ ] 新增更多語言支援

---

## 📦 打包與部署

### 建置 Wheel 套件

```bash
pip install wheel
python setup.py sdist bdist_wheel
```

### 安裝到系統

```bash
pip install dist/hashforge-1.0.0-py3-none-any.whl
```

---

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

1. Fork 本儲存庫
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 建立 Pull Request

### 提交規範

- `feat:` 新功能
- `fix:` 修復問題
- `docs:` 文件更新
- `refactor:` 程式碼重構
- `test:` 測試相關

---

## 📄 開源授權

本專案採用 [MIT License](LICENSE) 開源授權條款。

---

<p align="center">
  Made with ❤️ by HashForge Team
</p>
