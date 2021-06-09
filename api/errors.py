from enum import Enum

class ApiError(Enum):
    INVALID_HASHTAG = "INVALID_HASHTAG"
    INVALID_LOCATION = "INVALID_LOCATION"
    INVALID_TEXT = "INVALID_TEXT"
    INVALID_INPUT = "INVALID_INPUT"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    PROTECTED_USER = "PROTECTED_USER"

class TweepyError(Enum):
    INVALID_USER = 34
    INVALID_HASHTAG = 195
    PROTECTED_USER = "N"

class UnauthorizedUserRequestError(Exception):
    def __init__(self) -> None:
        self.msg = "Unauthorized request from anonymous user. You must be logged in."
        super().__init__(self.msg)
        