# File with constants for bot
import enum
from typing import List
from loguru import logger

logger.add("errors.log", format="{time} {level} {message}", level="ERROR")


class Ids(enum.Enum):
    """
    Class for some ID's
    """

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
    PERSONAL_DATA_MENU = enum.auto()
    REGISTRATION_MENU = enum.auto()
    CHECK_PROFILE_MENU = enum.auto()
    SEARCH_PARAMETERS_MENU = enum.auto()
    CHECK_SEARCH_PARAMETERS_MENU = enum.auto()
    SEARCH_MENU = enum.auto()
    PROFILE_REACTIONS_MENU = enum.auto()
    SUBSCRIPTION_MENU = enum.auto()


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


GO_TO_SUBSCRIPTION_MENU = "GO_TO_SUBSCRIPTION_MENU"

MAXIMUM_NUMBER_OF_LIKES = 100

link_to_yoomoney = "https://yoomoney.ru/to/410015159768343/0"


@enum.unique
class Items(enum.Enum):

    def get_str_value(self, dictionary: dict) -> str:
        try:
            return dictionary[self]
        except KeyError:
            logger.error(f"Can't find value for {self} in dictionary")
            return self.value

    def get_source_value(self) -> str:
        return self.value

    @staticmethod
    def get_object_by_str_value(str_value: str, dictionary: dict):
        for key, value in dictionary.items():
            if value == str_value:
                return key
        logger.error(f"Can't find object with value='{str_value}'")
        return None

    @classmethod
    def get_all_str_vales(cls, dictionary: dict) -> List[str]:
        """
        :return: list with all str values of enum's constants
        """
        result = []
        for member in cls.__members__.values():
            try:
                result.append(dictionary[member])
            except KeyError:
                logger.error(f"Can't find value for {member} in dictionary")
                result.append(member.value)
        return result


@enum.unique
class SpokenLanguages(Items):
    RUSSIAN = "russian"
    ENGLISH = "english"


@enum.unique
class ProgrammingLanguages(Items):
    PYTHON = "python"
    C = "c"
    CPP = "cpp"
    C_SHARP = "c_sharp"
    JAVA = "java"
    JAVA_SCRIPT = "java_script"
    SQL = "sql"
    PHP = "php"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    RUBY = "ruby"
    ASSEMBLER = "assembler"
    HTML_CSS = "html_css"
    NODE_JS = "node_js"


@enum.unique
class Interests(Items):
    DB_DESIGN = "db_design"
    FRONT_END = "front_end"
    BACK_END = "back_end"
    MACHINE_LEARNING = "machine_learning"
    BIG_DATA = "big_data"
    DEV_FOR_ANDROID = "android_dev"
    DEV_FOR_IOS = "ios_dev"
    DESIGN = "design"
    PROJECT_MANAGEMENT = "project_management"
    TESTING = "testing"


@enum.unique
class AgeGroups(Items):
    YOUNGER_THAN_14 = "younger_than_14"
    FROM_14_TO_18 = "from_14_to_18"
    FROM_18_TO_25 = "from_18_to_25"
    OLDER_THAN_25 = "older_than_25"


@enum.unique
class MainMenuItems(Items):
    FIND_PEOPLE = "find_people"
    SUBSCRIPTION = "subscription"
    FIND_PROJECT = "find_project"
    FIND_PEOPLE_TO_THE_PROJECT = "find_people_to_the_project"


@enum.unique
class SearchMenuItems(Items):
    FIND = "find"
    EDIT_SEARCH_PARAMETERS = "edit_search_parameters"
    GO_TO_MAIN_MENU = "go_to_main_menu"
    EDIT_PROFILE = "edit_profile"


@enum.unique
class ProfileReactionsMenu(Items):
    LIKE = "like"
    SKIP = "skip"
    GO_TO_MAIN_MENU = "go_to_main_menu"


@enum.unique
class AskPersonalData(Items):
    AGREE = "agree"
    REFUSE = "refuse"
