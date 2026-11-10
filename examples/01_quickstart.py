# 01_quickstart.py
from emochi import Emochi

# Khoi tao client Emochi (tu dong doc session neu co)
client = Emochi()

# Kiem tra trang thai dang nhap
if not client.is_authenticated:
    print("Vui long nhap access token de bat dau:")
    token = input("Token: ").strip()
    client.login_with_token(token)

user = client.get_profile()
print(f"Xin chao {user.username} (ID: {user.id})")
if user.email:
    print(f"Email: {user.email}")
print(f"Goi VIP/Premium: {user.is_premium}")
