# 04_interactive_cli.py
import sys
from emochi import Emochi, translate_en_to_vi

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    except Exception:
        pass

def main():
    client = Emochi()
    print("=" * 50)
    print("   EMOCHI AI CLIENT - INTERACTIVE CONSOLE")
    print("=" * 50)

    if not client.is_authenticated:
        print("Chua dang nhap. Vui long chon:")
        print("1. Gui ma OTP qua Email")
        print("2. Dan Access Token truc tiep")
        sub = input("Chon (1/2): ").strip()
        if sub == "1":
            em = input("Nhap email: ").strip()
            client.send_verification_code(em)
            otp = input("Nhap OTP (4 so): ").strip()
            u = client.login_with_email(em, otp)
            print(f"Dang nhap thanh cong: {u.username}")
        else:
            tok = input("Dan token: ").strip()
            u = client.login_with_token(tok)
            print(f"Xac thuc thanh cong: {u.username}")

    # Chon nhan vat
    print("\nChon nhan vat chat (Mac dinh: Borian Walker)")
    char_id = input("Nhap ID (Enter de chon Borian Walker): ").strip() or "X8a5E4t_TM1X2EnPkhTY_"
    char = client.get_character(char_id)
    
    print("\n" + "=" * 50)
    print(f"DA KET NOI VOI: {char.name}")
    print(f"Avatar CDN: {char.avatar_url}")
    print("Go '/exit' de thoat.")
    print("=" * 50)

    if char.welcome_message:
        print(f"\nAI: {char.welcome_message}")
        print(f"Dich: {translate_en_to_vi(char.welcome_message)}")

    conv = client.create_conversation(char)

    while True:
        try:
            msg = input("\nBan: ").strip()
            if not msg:
                continue
            if msg.lower() in ("/exit", "exit"):
                break

            print(f"\n{char.name}: ", end="", flush=True)
            reply = client.send_message(
                conversation=conv,
                content=msg,
                character=char,
                on_stream=lambda c: print(c, end="", flush=True),
                translate=True
            )
            print()
            if reply.translated_content:
                print(f"\n[Dich Tieng Viet]:\n{reply.translated_content}")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
