import requests
from typing import Optional
from ._config import BASE_URL
from ._exception import EmochiAuthError, EmochiApiError, EmochiNetworkError
from ._state import State
from .models.user import User

class AuthMixin:
    state: State

    def send_verification_code(self, email: str) -> bool:
        url = f"{BASE_URL}/auth/verify-email-code"
        headers = self.state.get_headers()
        payload = {"email": email.strip()}
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=15)
            if r.status_code in (200, 201):
                return True
            raise EmochiAuthError(f"Gửi mã OTP thất bại (HTTP {r.status_code}): {r.text}", r.status_code)
        except requests.RequestException as e:
            raise EmochiNetworkError(f"Lỗi mạng khi gửi OTP: {e}")

    def login_with_email(self, email: str, code: str) -> User:
        url = f"{BASE_URL}/auth/email-login"
        headers = self.state.get_headers()
        payload = {
            "email": email.strip(),
            "verificationCode": code.strip()
        }
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=15)
            if r.status_code == 200:
                data = r.json()
                token = data.get("encodedToken") or data.get("token")
                user_id = data.get("userId")
                if not token:
                    raise EmochiAuthError("Máy chủ không trả về access token.")
                self.state.token = token
                self.state.user_id = user_id
                # Tải thông tin người dùng
                user = self.get_profile()
                self.state.user = user
                self.state.save()
                return user
            else:
                raise EmochiAuthError(f"Đăng nhập thất bại (HTTP {r.status_code}): {r.text}", r.status_code)
        except requests.RequestException as e:
            raise EmochiNetworkError(f"Lỗi mạng khi đăng nhập: {e}")

    def login_with_token(self, token: str) -> User:
        clean_token = token.strip()
        if clean_token.startswith("Bearer "):
            clean_token = clean_token[7:].strip()
        self.state.token = clean_token
        user = self.get_profile()
        self.state.user = user
        self.state.user_id = user.id
        self.state.save()
        return user

    def get_profile(self) -> User:
        if not self.state.token:
            raise EmochiAuthError("Chưa đăng nhập! Cần token hợp lệ.")
        url = f"{BASE_URL}/user/profile"
        headers = self.state.get_headers()
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                data = r.json()
                user_data = data.get("data", data)
                return User.from_dict(user_data)
            raise EmochiAuthError(f"Không thể lấy profile (HTTP {r.status_code}): {r.text}", r.status_code)
        except requests.RequestException as e:
            raise EmochiNetworkError(f"Lỗi mạng khi lấy profile: {e}")

    def logout(self):
        self.state.clear()
