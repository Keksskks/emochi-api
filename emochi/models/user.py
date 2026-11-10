from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class User:
    id: str
    username: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    is_premium: bool = False
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        if not data:
            return cls(id="", username="Guest")
        return cls(
            id=data.get("id") or data.get("userId") or "",
            username=data.get("name") or data.get("username") or "User",
            email=data.get("email"),
            avatar_url=data.get("image") or data.get("avatar"),
            is_premium=bool(data.get("is_premium") or data.get("isPremium", False)),
            created_at=data.get("createdAt")
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "avatar_url": self.avatar_url,
            "is_premium": self.is_premium,
            "created_at": self.created_at
        }
