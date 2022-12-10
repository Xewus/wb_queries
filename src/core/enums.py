from enum import Enum, StrEnum


class BetterEnum(Enum):
    @classmethod
    def values(cls) -> list:
        return [attr.value for attr in cls]

    @classmethod
    def as_dict(cls) -> dict:
        return {attr.name: attr.value for attr in cls}


class Commands(StrEnum, BetterEnum):
    START = 'start'
    HELP = 'help'
    SEARCH = 'search'


class CallBackData(StrEnum):
    OFFCOURSE = 'OffCourse'
