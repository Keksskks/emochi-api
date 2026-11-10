from ._client import Emochi, EmochiClient
from ._exception import (
    EmochiException,
    EmochiAuthError,
    EmochiApiError,
    EmochiNetworkError,
    EmochiCharacterNotFound,
    EmochiRateLimitError
)
from .models.character import Character
from .models.user import User
from .models.message import Message
from .models.conversation import Conversation
from .utils.translator import translate_en_to_vi

__title__ = "emochi"
__version__ = "1.0.0"
__author__ = "xellox"
__email__ = "truong77kk@gmail.com"
__license__ = "MIT"

__all__ = [
    "Emochi",
    "EmochiClient",
    "EmochiException",
    "EmochiAuthError",
    "EmochiApiError",
    "EmochiNetworkError",
    "EmochiCharacterNotFound",
    "EmochiRateLimitError",
    "Character",
    "User",
    "Message",
    "Conversation",
    "translate_en_to_vi"
]
