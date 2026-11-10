from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from .message import Message

@dataclass
class Conversation:
    id: str
    prompt_id: str
    character_name: str = ""
    messages: List[Message] = field(default_factory=list)
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Conversation":
        messages = [
            Message.from_dict(m) if isinstance(m, dict) else m 
            for m in data.get("messages", [])
        ]
        return cls(
            id=data.get("id") or "",
            prompt_id=data.get("promptId") or "",
            character_name=data.get("character_name") or data.get("title") or "",
            messages=messages,
            created_at=data.get("createdAt")
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "prompt_id": self.prompt_id,
            "character_name": self.character_name,
            "messages": [m.to_dict() for m in self.messages],
            "created_at": self.created_at
        }
