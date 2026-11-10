import requests
import json
import uuid
import time
import websocket
from typing import Optional, Callable, Union
from ._config import BASE_URL, WS_BASE_URL, DEFAULT_MODEL
from ._exception import EmochiAuthError, EmochiApiError, EmochiNetworkError
from ._state import State
from .models.character import Character
from .models.conversation import Conversation
from .models.message import Message
from .utils.translator import translate_en_to_vi

class ChatMixin:
    state: State

    def send_message(
        self,
        conversation: Union[Conversation, str],
        content: str,
        character: Optional[Union[Character, str]] = None,
        model: str = DEFAULT_MODEL,
        temperature: float = 0.7,
        on_stream: Optional[Callable[[str], None]] = None,
        translate: bool = False
    ) -> Message:
        if not self.state.token:
            raise EmochiAuthError("Cần đăng nhập tài khoản trước khi gửi tin nhắn.")

        conv_id = conversation.id if isinstance(conversation, Conversation) else conversation
        prompt_id = None
        if isinstance(conversation, Conversation):
            prompt_id = conversation.prompt_id
        elif isinstance(character, Character):
            prompt_id = character.id
        elif isinstance(character, str):
            prompt_id = character
        elif self.state.selected_character_id:
            prompt_id = self.state.selected_character_id

        if not prompt_id:
            raise EmochiApiError("Thiếu prompt_id của nhân vật.")

        msg_id = str(uuid.uuid4())
        chunks_collected = []

        # 1. Thử gửi qua WebSocket để nhận streaming theo thời gian thực
        try:
            ws_url = f"{WS_BASE_URL}/socket.io/?EIO=4&transport=websocket"
            ws = websocket.create_connection(ws_url, timeout=10)

            # Đợi bắt tay kết nối (Engine.IO)
            ws.recv()
            ws.send(f'40{{"token":"Bearer {self.state.token}"}}')

            payload = {
                "conversationId": conv_id,
                "promptId": prompt_id,
                "question": content,
                "model": model,
                "temperature": temperature,
                "streamReply": True,
                "nsfw": False,
                "messageId": msg_id
            }
            ws.send(f'42["chat",{json.dumps(payload)}]')

            start_time = time.time()
            while time.time() - start_time < 30:
                frame = ws.recv()
                if not frame:
                    break
                if frame == "2":
                    ws.send("3")  # Ping-Pong
                    continue
                if frame.startswith("42"):
                    data_str = frame[2:]
                    event_data = json.loads(data_str)
                    if isinstance(event_data, list) and len(event_data) >= 2:
                        event_name = event_data[0]
                        payload_data = event_data[1]

                        if event_name in ("chatStream", "chat"):
                            chunk = payload_data.get("chunk") or payload_data.get("delta") or ""
                            if chunk:
                                chunks_collected.append(chunk)
                                if on_stream:
                                    on_stream(chunk)

                            if payload_data.get("isLast") or payload_data.get("finish"):
                                break
            ws.close()
        except Exception:
            pass

        full_reply = "".join(chunks_collected)

        # 2. Nếu WebSocket không nhận được nội dung, sử dụng REST API /v4/chat
        if not full_reply.strip():
            url = f"{BASE_URL}/v4/chat"
            headers = self.state.get_headers()
            body = {
                "conversationId": conv_id,
                "promptId": prompt_id,
                "question": content,
                "model": model,
                "temperature": temperature,
                "streamReply": False,
                "nsfw": False,
                "messageId": msg_id
            }
            try:
                r = requests.post(url, json=body, headers=headers, timeout=30)
                if r.status_code == 200:
                    resp_json = r.json()
                    full_reply = resp_json.get("content") or resp_json.get("reply") or resp_json.get("data") or ""
                    if on_stream and full_reply:
                        on_stream(full_reply)
                else:
                    raise EmochiApiError(f"Lỗi gửi tin nhắn (HTTP {r.status_code}): {r.text}", r.status_code)
            except requests.RequestException as e:
                raise EmochiNetworkError(f"Lỗi mạng khi gửi tin nhắn: {e}")

        # 3. Tự động dịch sang tiếng Việt nếu được yêu cầu
        translated_text = None
        if translate and full_reply:
            try:
                translated_text = translate_en_to_vi(full_reply)
            except Exception:
                pass

        return Message(
            id=msg_id,
            role="assistant",
            content=full_reply,
            translated_content=translated_text,
            prompt_id=prompt_id,
            created_at=str(int(time.time() * 1000))
        )
