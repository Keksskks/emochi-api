from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

@dataclass
class Character:
    id: str
    name: str
    description: str = ""
    welcome_message: str = ""
    init_prompt: str = ""
    avatar_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    background_url: Optional[str] = None
    author_avatar_url: Optional[str] = None
    voice_preview_url: Optional[str] = None
    category: str = "General"
    tags: List[str] = field(default_factory=list)
    uses: int = 0
    upvotes: int = 0
    model: str = "Vanilla V3"
    temperature: float = 0.7

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Character":
        if not data:
            return cls(id="", name="Unknown")
        
        char_id = data.get("id") or data.get("promptId") or ""
        name = data.get("title") or data.get("name") or "Unnamed"
        desc = data.get("description") or ""
        welcome = data.get("welcomeMessage") or data.get("rawWelcomeMessage") or ""
        init_p = data.get("initPrompt") or ""
        avatar = data.get("coverURL") or data.get("avatar") or data.get("thumbnailURL") or None
        thumb = data.get("thumbnailURL") or avatar
        bg = data.get("backgroundURL") or data.get("background") or None
        cat = data.get("category") or "Roleplay"

        user_info = data.get("User") or data.get("author") or {}
        author_avatar = user_info.get("image") if isinstance(user_info, dict) else None

        speaker_info = data.get("speaker") or {}
        voice_url = speaker_info.get("preview") if isinstance(speaker_info, dict) else None
        
        tags_raw = data.get("tags") or data.get("Tag") or []
        tags = [t if isinstance(t, str) else t.get("name", "") for t in tags_raw] if isinstance(tags_raw, list) else []

        return cls(
            id=char_id,
            name=name,
            description=desc,
            welcome_message=welcome,
            init_prompt=init_p,
            avatar_url=avatar,
            thumbnail_url=thumb,
            background_url=bg,
            author_avatar_url=author_avatar,
            voice_preview_url=voice_url,
            category=cat,
            tags=tags,
            uses=int(data.get("uses", 0)),
            upvotes=int(data.get("upvotes", 0)),
            model=data.get("model") or "Vanilla V3",
            temperature=float(data.get("temperature", 0.7))
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "welcome_message": self.welcome_message,
            "avatar_url": self.avatar_url,
            "thumbnail_url": self.thumbnail_url,
            "background_url": self.background_url,
            "author_avatar_url": self.author_avatar_url,
            "voice_preview_url": self.voice_preview_url,
            "category": self.category,
            "tags": self.tags,
            "uses": self.uses,
            "upvotes": self.upvotes,
            "model": self.model,
            "temperature": self.temperature
        }
