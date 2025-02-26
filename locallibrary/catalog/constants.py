from enum import Enum

CHAR_MAX_LENGTH = 200
TEXT_MAX_LENGTH = 1000
ISBN_MAX_LENGTH = 13
STATUS_MAX_LENGTH = 1


class BookStatus(Enum):
    MAINTENANCE = "m"
    ON_LOAN = "o"
    AVAILABLE = "a"
    RESERVED = "r"
