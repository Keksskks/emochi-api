import json
import os
import uuid
from typing import Optional, Dict, Any
from ._config import get_default_headers, generate_signature_headers
from .models.user import User

class State:
    def __init__(self, session_path: Optional[str] = None):
        self.session_path = session_path or os.path.join(os.getcwd(), ".emochi_session.json")
        self.device_id: str = str(uuid.uuid4())
        self.token: Optional[str] = None
        self.user_id: Optional[str] = None
        self.user: Optional[User] = None
        self.selected_character_id: Optional[str] = None
        self.load()

    def is_authenticated(self) -> bool:
        return bool(self.token)

    def get_headers(self) -> Dict[str, str]:
        headers = get_default_headers(self.device_id)
        if self.token:
            sig_headers = generate_signature_headers(self.token)
            headers.update(sig_headers)
        return headers

    def load(self):
        if os.path.exists(self.session_path):
            try:
                with open(self.session_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.device_id = data.get("device_id") or self.device_id
                    self.token = data.get("token")
                    self.user_id = data.get("user_id")
                    self.selected_character_id = data.get("selected_character_id")
                    if data.get("user"):
                        self.user = User.from_dict(data["user"])
            except Exception:
                pass

    def save(self):
        try:
            os.makedirs(os.path.dirname(os.path.abspath(self.session_path)), exist_ok=True)
            data = {
                "device_id": self.device_id,
                "token": self.token,
                "user_id": self.user_id,
                "selected_character_id": self.selected_character_id,
                "user": self.user.to_dict() if self.user else None
            }
            with open(self.session_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def clear(self):
        self.token = None
        self.user_id = None
        self.user = None
        self.selected_character_id = None
        if os.path.exists(self.session_path):
            try:
                os.remove(self.session_path)
            except Exception:
                pass
