class EmochiException(Exception):
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def __str__(self):
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message

class EmochiAuthError(EmochiException):
    pass

class EmochiApiError(EmochiException):
    pass

class EmochiNetworkError(EmochiException):
    pass

class EmochiCharacterNotFound(EmochiException):
    pass

class EmochiRateLimitError(EmochiException):
    pass
