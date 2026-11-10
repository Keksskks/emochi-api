# 02_chat_with_borian.py
from emochi import Emochi, translate_en_to_vi

client = Emochi()

# Lay thong tin Borian Walker bang Prompt ID
borian_id = "X8a5E4t_TM1X2EnPkhTY_"
borian = client.get_character(borian_id)

print("=" * 50)
print(f"Nhan vat: {borian.name}")
print(f"ID: {borian.id}")
print(f"Avatar CDN: {borian.avatar_url}")
if borian.voice_preview_url:
    print(f"Giong noi mau (Audio): {borian.voice_preview_url}")
print("=" * 50)

# Hien thi loi chao goc va ban dich tieng Viet
if borian.welcome_message:
    print("\nLoi chao goc (EN):")
    print(borian.welcome_message)
    print("\nLoi chao dich tieng Viet:")
    print(translate_en_to_vi(borian.welcome_message))

print("\nBat dau tro chuyen voi Borian Walker...")
message_text = "Who are you and why did Victor choose you?"
print(f"\nBan: {message_text}")
print(f"{borian.name} (Real-time Stream): ", end="", flush=True)

# Callback streaming token
def stream_handler(chunk: str):
    print(chunk, end="", flush=True)

reply = client.chat(
    character=borian,
    message=message_text,
    on_stream=stream_handler,
    translate=True
)
print()

# In ban dich tieng Viet
if reply.translated_content:
    print("\n" + "=" * 50)
    print("BAN DICH TIENG VIET:")
    print(reply.translated_content)
    print("=" * 50)
