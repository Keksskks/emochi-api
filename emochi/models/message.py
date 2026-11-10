from dataclasses import dataclass
from typing import Optional, Dict, Any
import time

@dataclass
class Message:
    id: str
    role: str  # 'user' hoặc 'assistant'
    content: str
    translated_content: Optional[str] = None
    prompt_id: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        return cls(
            id=data.get("id") or str(int(time.time() * 1000)),
            role=data.get("role") or ("user" if data.get("isUser") else "assistant"),
            content=data.get("content") or data.get("text") or "",
            translated_content=data.get("translated_content"),
            prompt_id=data.get("promptId"),
            created_at=data.get("createdAt")
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "translated_content": self.translated_content,
            "prompt_id": self.prompt_id,
            "created_at": self.created_at
        }
