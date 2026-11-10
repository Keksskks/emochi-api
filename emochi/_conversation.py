import requests
import json
import os
from typing import List, Optional, Union
from ._config import BASE_URL
from ._exception import EmochiAuthError, EmochiApiError, EmochiNetworkError
from ._state import State
from .models.character import Character
from .models.conversation import Conversation
from .models.message import Message

class ConversationMixin:
    state: State

    def create_conversation(self, character: Union[Character, str]) -> Conversation:
        if not self.state.token:
            raise EmochiAuthError("Cần đăng nhập tài khoản để khởi tạo hội thoại.")

        prompt_id = character.id if isinstance(character, Character) else character
        char_name = character.name if isinstance(character, Character) else ""

        url = f"{BASE_URL}/conversation/create"
        headers = self.state.get_headers()
        payload = {
            "promptId": prompt_id,
            "location": "UNKNOWN",
            "live": True,
            "messages": []
        }

        try:
            r = requests.post(url, json=payload, headers=headers, timeout=15)
            if r.status_code in (200, 201):
                data = r.json()
                conv_id = data.get("id")
                conv = Conversation(
                    id=conv_id,
                    prompt_id=prompt_id,
                    character_name=char_name,
                    created_at=data.get("createdAt")
                )
                self.state.selected_character_id = prompt_id
                self.state.save()
                return conv
            else:
                raise EmochiApiError(f"Lỗi tạo hội thoại (HTTP {r.status_code}): {r.text}", r.status_code)
        except requests.RequestException as e:
            raise EmochiNetworkError(f"Lỗi kết nối khi tạo hội thoại: {e}")

    def get_conversation_history(self, prompt_id: str, take: int = 20) -> List[Message]:
        if not self.state.token:
            raise EmochiAuthError("Cần đăng nhập để tải lịch sử hội thoại.")

        url = f"{BASE_URL}/conversation/latest"
        headers = self.state.get_headers()
        params = {"promptId": prompt_id, "take": take}
        try:
            r = requests.get(url, params=params, headers=headers, timeout=15)
            if r.status_code == 200:
                data = r.json()
                msgs_raw = data.get("messages") or data.get("data") or []
                return [Message.from_dict(m) for m in msgs_raw]
            return []
        except requests.RequestException:
            return []
