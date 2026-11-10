from typing import Optional, Union, Callable
from ._state import State
from ._auth import AuthMixin
from ._character import CharacterMixin
from ._conversation import ConversationMixin
from ._chat import ChatMixin
from .models.character import Character
from .models.conversation import Conversation
from .models.message import Message

class Emochi(AuthMixin, CharacterMixin, ConversationMixin, ChatMixin):
    def __init__(self, token: Optional[str] = None, session_path: Optional[str] = None):
        self.state = State(session_path=session_path)
        if token:
            self.login_with_token(token)

    @property
    def is_authenticated(self) -> bool:
        return self.state.is_authenticated()

    @property
    def current_user(self):
        return self.state.user

    def chat(
        self,
        character: Union[Character, str],
        message: str,
        conversation: Optional[Union[Conversation, str]] = None,
        on_stream: Optional[Callable[[str], None]] = None,
        translate: bool = False
    ) -> Message:
        char_obj = character if isinstance(character, Character) else self.get_character(character)
        
        conv = conversation
        if not conv:
            conv = self.create_conversation(char_obj)

        return self.send_message(
            conversation=conv,
            content=message,
            character=char_obj,
            on_stream=on_stream,
            translate=translate
        )

# Alias tương thích
EmochiClient = Emochi
