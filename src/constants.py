# File with constants for bot
import enum
from typing import List


class Ids(enum.Enum):
    "Class for some ID's"

    @classmethod
    def get_all_not_null_ids(cls) -> List[enum.Enum]:
        return [member for member in cls if member.name != "NULL"]


@enum.unique
class MenuIds(Ids):
    """
    IDs of bots menus
    """
    NULL = enum.auto()
    MAIN_MENU = enum.auto()
    REGISTRATION_MENU = enum.auto()
    CHECK_PROFILE_MENU = enum.auto()
    SEARCH_PARAMETERS_MENU = enum.auto()
    CHECK_SEARCH_PARAMETERS_MENU = enum.auto()
    SEARCH_MENU = enum.auto()
    PROFILE_REACTIONS_MENU = enum.auto()


@enum.unique
class ProfileItemsIds(Ids):
    """
    IDs of user's profile items
    """
    NULL = enum.auto()
    FIRST_NAME = enum.auto()
    LAST_NAME = enum.auto()
    AGE = enum.auto()
    SPOKEN_LANGUAGES = enum.auto()
    PROGRAMMING_LANGUAGES = enum.auto()
    INTERESTS = enum.auto()


@enum.unique
class SearchParametersItemsIds(Ids):
    """
    IDs of user's search parameters items
    """
    NULL = enum.auto()
    AGE_GROUP = enum.auto()
    SPOKEN_LANGUAGES = enum.auto()
    PROGRAMMING_LANGUAGES = enum.auto()
    INTERESTS = enum.auto()


PROFILE_REACTIONS_MENU_PREFIX = "PROFILE_REACTIONS_"

MAXIMUM_NUMBER_OF_LIKES = 3
