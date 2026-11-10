<div align="center">

# 🤖 Emochi API Client for Python

<p align="center">
  <b>Thư viện Python API Client không chính thức (Unofficial SDK) cho nền tảng Emochi / FlowGPT AI Character Chat.</b>
</p>

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Keksskks%2Femochi--api-181717.svg?logo=github)](https://github.com/Keksskks/emochi-api)
[![Author: xellox](https://img.shields.io/badge/Author-xellox-orange.svg)](mailto:truong77kk@gmail.com)

</div>

---

## 📌 Giới thiệu

**`emochi-api`** là một thư viện Python mạnh mẽ, gọn nhẹ và dễ sử dụng, được xây dựng dựa trên cơ chế Reverse Engineering các giao thức mạng của ứng dụng Emochi Android (FlowGPT Mobile).

Thư viện hỗ trợ đầy đủ các tính năng:
- 🔐 **Xác thực toàn diện:** Gửi mã OTP xác thực qua Email, đăng nhập trực tiếp bằng Bearer JWT Token, tự động duy trì phiên làm việc.
- 🎭 **Khám phá kho AI đa dạng:** Lấy danh sách hàng trăm nhân vật AI từ Bảng xếp hạng thịnh hành (*Daily, Weekly, Monthly*), 12 thể loại phổ biến (*Romance, Drama, Comedy, Dark Romance, v.v.*) và tìm kiếm theo từ khóa.
- 🖼️ **Trích xuất hình ảnh trực tiếp (CDN):** Tự động bóc tách link Cover Avatar, Thumbnail, Background và mẫu Audio giọng nói của nhân vật.
- ⚡ **Chat thời gian thực (Streaming):** Hỗ trợ WebSocket / Socket.IO nhận streaming từng token phản hồi trực tiếp từ AI.
- 🌐 **Tự động dịch song ngữ (EN ➔ VI):** Tích hợp công cụ dịch tự động phản hồi tiếng Anh của AI sang tiếng Việt mượt mà với bộ nhớ đệm thông minh.

---

## 🚀 Cài đặt

Cài đặt trực tiếp từ kho lưu trữ GitHub:

```bash
pip install git+https://github.com/Keksskks/emochi-api.git
```

Hoặc cài đặt từ mã nguồn cục bộ:

```bash
git clone https://github.com/Keksskks/emochi-api.git
cd emochi-api
pip install -r requirements.txt
pip install -e .
```

---

## 💡 Hướng dẫn nhanh (Quick Start)

### 1. Đăng nhập và bắt đầu trò chuyện với Borian Walker

```python
from emochi import Emochi

# Khởi tạo client
client = Emochi(token="your_bearer_token_here")

# Lấy thông tin nhân vật Borian Walker
borian = client.get_character("X8a5E4t_TM1X2EnPkhTY_")
print(f"Nhân vật: {borian.name}")
print(f"Ảnh đại diện CDN: {borian.avatar_url}")

# Gửi tin nhắn và tự động dịch câu trả lời sang tiếng Việt
reply = client.chat(
    character=borian,
    message="Who are you and why are you here?",
    translate=True
)

print("AI (English):", reply.content)
print("Bản dịch Tiếng Việt:", reply.translated_content)
```

---

### 2. Nhận phản hồi Streaming thời gian thực

```python
from emochi import Emochi

client = Emochi(token="your_bearer_token_here")
borian = client.get_character("X8a5E4t_TM1X2EnPkhTY_")

print(f"{borian.name}: ", end="", flush=True)

# Định nghĩa hàm callback nhận token
def on_stream(chunk: str):
    print(chunk, end="", flush=True)

reply = client.chat(
    character=borian,
    message="Tell me about your background.",
    on_stream=on_stream,
    translate=True
)

# Hiển thị bản dịch sau khi streaming kết thúc
if reply.translated_content:
    print("\n\n[Dịch Tiếng Việt]:")
    print(reply.translated_content)
```

---

### 3. Lấy tất cả các nhân vật AI & Link ảnh CDN

```python
from emochi import Emochi

client = Emochi()

# Lấy tổng hợp 50 nhân vật AI khác nhau (khử trùng lặp)
characters = client.get_all_characters(max_total=50)

for i, char in enumerate(characters, 1):
    print(f"[{i}] {char.name} ({char.category})")
    print(f"     ID: {char.id}")
    print(f"     Ảnh: {char.avatar_url}")
    print(f"     Mô tả: {char.description[:60]}...")
    print("-" * 50)
```

---

### 4. Tìm kiếm nhân vật theo từ khóa

```python
from emochi import Emochi

client = Emochi()

# Tìm kiếm nhân vật theo chủ đề 'yandere'
results = client.search_characters("yandere", take=10)

for char in results:
    print(f"Name: {char.name} | ID: {char.id} | Avatar: {char.avatar_url}")
```

---

## 📖 Bảng tra cứu API (API Reference)

### Class `Emochi` / `EmochiClient`

| Phương thức | Tham số | Mô tả |
| :--- | :--- | :--- |
| `send_verification_code(email)` | `email: str` | Gửi mã OTP xác thực (4 số) qua email |
| `login_with_email(email, code)` | `email: str, code: str` | Đăng nhập tài khoản bằng mã OTP |
| `login_with_token(token)` | `token: str` | Đăng nhập bằng JWT Bearer Token |
| `get_profile()` | *Không* | Lấy thông tin tài khoản hiện tại |
| `get_character(prompt_id)` | `prompt_id: str` | Lấy chi tiết nhân vật (avatar, lời chào, bối cảnh) |
| `get_all_characters(max_total)` | `max_total: int = 250` | Lấy toàn bộ nhân vật AI từ các bảng xếp hạng & tag |
| `get_ranking(take, period)` | `take: int, period: str` | Lấy bảng xếp hạng (`daily`, `weekly`, `monthly`) |
| `get_characters_by_tags(take)` | `take: int = 20` | Lấy nhân vật chia theo 12 thể loại |
| `search_characters(query, take)` | `query: str, take: int` | Tìm kiếm nhân vật qua search v2 |
| `create_conversation(character)` | `character: Character\|str` | Tạo phiên hội thoại mới với nhân vật |
| `chat(character, message, ...)` | `character, message, on_stream, translate` | Gửi tin nhắn cấp cao (hỗ trợ stream & dịch tự động) |
| `send_message(...)` | `conversation, content, ...` | Gửi tin nhắn qua WebSocket hoặc REST |

---

## 📂 Cấu trúc Repository

```text
emochi-api/
├── emochi/                        # Core Library Package
│   ├── __init__.py                # Package exports
│   ├── _client.py                 # Main Emochi Client class
│   ├── _auth.py                   # Authentication mixin (OTP & Token)
│   ├── _character.py              # Character browsing & search
│   ├── _conversation.py           # Conversation manager
│   ├── _chat.py                   # Real-time WebSocket & REST engine
│   ├── _config.py                 # Security signatures & headers
│   ├── _state.py                  # Session state persistence
│   ├── _exception.py              # Custom exceptions
│   ├── models/                    # Data models (Character, User, Message, Conversation)
│   └── utils/                     # Utilities (Translator & Logger)
├── examples/                      # Runnable sample scripts
│   ├── 01_quickstart.py
│   ├── 02_chat_with_borian.py
│   ├── 03_browse_all_ai.py
│   └── 04_interactive_cli.py
├── tests/                         # Unit tests
├── LICENSE                        # MIT License
├── README.md                      # Documentation
├── pyproject.toml                 # Build system configuration
├── requirements.txt               # Dependencies
└── setup.py                       # Setuptools installation
```

---

## 👨‍💻 Thông tin Tác giả

- **Tác giả:** xellox
- **Email:** [truong77kk@gmail.com](mailto:truong77kk@gmail.com)
- **GitHub:** [https://github.com/Keksskks/emochi-api](https://github.com/Keksskks/emochi-api)

---

## 📄 Giấy phép (License)

Dự án này được phát hành dưới giấy phép [MIT License](LICENSE).
Mọi quyền đóng góp và sử dụng mã nguồn cho mục đích học tập, nghiên cứu đều được chào đón!
