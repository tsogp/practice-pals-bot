import enum


class MenuIds(enum.Enum):
    MAIN_MENU = enum.auto()
    REGISTRATION_MENU = enum.auto()
    CHECK_PROFILE_MENU = enum.auto()
    SEARCH_PARAMETERS_MENU = enum.auto()


class ProfileItemsIds(enum.Enum):
    NULL = enum.auto()
    FIRST_NAME = enum.auto()
    LAST_NAME = enum.auto()
    AGE = enum.auto()
    SPOKEN_LANGUAGES = enum.auto()
    PROGRAMMING_LANGUAGES = enum.auto()
    INTERESTS = enum.auto()


class SearchParametersItemsIds(enum.Enum):
    NULL = enum.auto()
    AGE_GROUP = enum.auto()


MAIN_MENU_PREFIX = "main_menu_"
