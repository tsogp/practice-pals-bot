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

@enum.unique
class PossibleAnswers(enum.Enum):

    @classmethod
    def is_member_of_enum(cls, value: str) -> bool:
        """
        :return: does the enumeration contain a value
        """
        values = [member.value for name, member in cls.__members__.items()]
        return value in values

    @classmethod
    def get_all_vales(cls) -> List[str]:
        """
        :return: list with all values of enum's constants
        """
        return [member.value for name, member in cls.__members__.items()]

    def __str__(self) -> str:
        return self.value


@enum.unique
class SpokenLanguages(PossibleAnswers):
    RUSSIAN = "russian"
    ENGLISH = "english"


@enum.unique
class ProgrammingLanguages(PossibleAnswers):
    PYTHON = "python"
    C = "c"
    CPP = "cpp"
    C_SHARP = "c_sharp"
    JAVA = "java"
    JAVA_SCRIPT = "java_script"


@enum.unique
class Interests(PossibleAnswers):
    FRONT_END = "front_end"
    BACK_END = "back_end"
    MACHINE_LEARNING = "machine_learning"
    BIG_DATA = "big_data"
    DEV_FOR_ANDROID = "android_dev"
    DEV_FOR_IOS = "ios_dev"


@enum.unique
class AgeGroups(PossibleAnswers):
    YOUNGER_THAN_14 = "younger_than_14"
    FROM_14_TO_18 = "from_14_to_18"
    FROM_18_TO_25 = "from_18_to_25"
    OLDER_THAN_25 = "older_than_25"
