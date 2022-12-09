from enum import Enum, StrEnum


class Commands(StrEnum):
    START = 'start'
    HELP = 'help'
    SEARCH = 'search'


class CallBackData(StrEnum):
    OFFCOURSE = 'OffCourse'
