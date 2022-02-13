import enum
from typing import Optional, List
import bottoken
from IDatabase import IDatabase

import constants

# SETTINGS FOR DEVELOPMENT AND MANUAL TESTING


TELEGRAM_ID: int = bottoken.ID  # Set your Telegram ID for manual testsing
IS_REGISTERED: bool = True
ARE_SEARCH_PARAMETERS_FILLED: bool = True
HAVE_SUBSCRIPTION: bool = False


# SETTINGS FOR DEVELOPMENT AND MANUAL TESTING


class UserProfile:
    """
    Profile of user for fake DB
    """
    __ID_COUNTER = 0  # For generating unique id

    def __init__(self,
                 telegram_login: str,
                 first_name: str,
                 last_name: str,
                 age: int,
                 spoken_languages: Optional[List[constants.SpokenLanguages]],
                 programming_languages: Optional[List[constants.ProgrammingLanguages]],
                 interests: Optional[List[constants.Interests]]):
        self.id = UserProfile.__ID_COUNTER
        UserProfile.__ID_COUNTER += 1
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.spoken_languages = spoken_languages
        self.programming_languages = programming_languages
        self.interests = interests
        self.telegram_login = telegram_login


class FakeDatabase(IDatabase):
    """
    Fake database for development (do not use in production)"
    """
    USERS_LIST: List[UserProfile] = []

    @classmethod
    def __add_users_to_users_list(cls) -> None:

        cls.USERS_LIST.append(UserProfile("user_ivan",
                                          "Иван",
                                          "Петров",
                                          12,
                                          [constants.SpokenLanguages.RUSSIAN],
                                          [constants.ProgrammingLanguages.PYTHON],
                                          [constants.Interests.DEV_FOR_IOS]))

        cls.USERS_LIST.append(UserProfile("user_pavel",
                                          "Павел",
                                          "Иванов",
                                          18,
                                          [constants.SpokenLanguages.ENGLISH],
                                          [constants.ProgrammingLanguages.PYTHON],
                                          [constants.Interests.BACK_END]))

        cls.USERS_LIST.append(UserProfile("user_misha",
                                          "Михаил",
                                          "Михайлов",
                                          15,
                                          [constants.SpokenLanguages.ENGLISH],
                                          [constants.ProgrammingLanguages.PYTHON],
                                          [constants.Interests.FRONT_END]))

        cls.USERS_LIST.append(UserProfile("user_evgen",
                                          "Евгений",
                                          "Баженов",
                                          30,
                                          [constants.SpokenLanguages.RUSSIAN],
                                          [constants.ProgrammingLanguages.PYTHON, constants.ProgrammingLanguages.C,
                                           constants.ProgrammingLanguages.CPP],
                                          [constants.Interests.BACK_END, constants.Interests.BIG_DATA,
                                           constants.Interests.MACHINE_LEARNING]))

        cls.USERS_LIST.append(UserProfile("user_fedor",
                                          "Фёдор",
                                          "Котов",
                                          19,
                                          [constants.SpokenLanguages.ENGLISH],
                                          [constants.ProgrammingLanguages.PYTHON,
                                           constants.ProgrammingLanguages.C_SHARP,
                                           constants.ProgrammingLanguages.CPP],
                                          [constants.Interests.BACK_END]))

    def __init__(self):
        FakeDatabase.__add_users_to_users_list()
        self.__id: int = TELEGRAM_ID
        self.__telegram_login: str = "None"
        self.__telegram_id: int = 0
        self.__is_registered: bool = IS_REGISTERED
        self.__are_search_parameters_filled = ARE_SEARCH_PARAMETERS_FILLED
        self.__subscription = HAVE_SUBSCRIPTION

        self.__navigation: dict = {
            NavigationItems.MENU_ID: constants.MenuIds.NULL,
            NavigationItems.REGISTRATION_ITEM_ID: constants.ProfileItemsIds.NULL,
            NavigationItems.SEARCH_PARAMETER_ITEM_ID: constants.SearchParametersItemsIds.NULL
        }

        self.__profile: dict = {
            constants.ProfileItemsIds.FIRST_NAME: None,
            constants.ProfileItemsIds.LAST_NAME: None,
            constants.ProfileItemsIds.AGE: None,
            constants.ProfileItemsIds.SPOKEN_LANGUAGES: None,
            constants.ProfileItemsIds.PROGRAMMING_LANGUAGES: None,
            constants.ProfileItemsIds.INTERESTS: None
        }

        self.__search_parameters: dict = {
            constants.SearchParametersItemsIds.AGE_GROUP: None,
            constants.SearchParametersItemsIds.SPOKEN_LANGUAGES: None,
            constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES: None,
            constants.SearchParametersItemsIds.INTERESTS: None
        }
        self.__potential_relationships = []

        self.__number_of_likes: int = 0
        self.__last_profile_id: Optional[int] = None

    # REGISTRATION AND PROFILE

    def initial_user_setup(self, user_id: int) -> None:
        pass

    def is_registered(self, user_id: int) -> bool:
        return self.__is_registered

    def register_user(self, user_id: int) -> None:
        self.__is_registered = True

    def get_users_menu_id(self, user_id: int) -> constants.MenuIds:
        return self.__navigation[NavigationItems.MENU_ID]

    def set_users_menu_id(self, user_id: int, new_menu_id: constants.MenuIds) -> None:
        self.__navigation[NavigationItems.MENU_ID] = new_menu_id

    def get_users_registration_item_id(self, user_id: int) -> constants.ProfileItemsIds:
        return self.__navigation[NavigationItems.REGISTRATION_ITEM_ID]

    def set_users_registration_item_id(self, user_id: int, new_registration_item_id: constants.ProfileItemsIds) -> None:
        self.__navigation[NavigationItems.REGISTRATION_ITEM_ID] = new_registration_item_id

    # PROFILE

    def get_users_profile_first_name(self, user_id: int) -> str:
        if user_id == self.__id:
            return self.__profile[constants.ProfileItemsIds.FIRST_NAME]
        else:
            return self.USERS_LIST[user_id].first_name

    def set_users_profile_first_name(self, user_id: int, value: str) -> None:
        self.__profile[constants.ProfileItemsIds.FIRST_NAME] = value

    def get_users_profile_last_name(self, user_id: int) -> str:
        if user_id == self.__id:
            return self.__profile[constants.ProfileItemsIds.LAST_NAME]
        else:
            return self.USERS_LIST[user_id].last_name

    def set_users_profile_last_name(self, user_id: int, value: str) -> None:
        self.__profile[constants.ProfileItemsIds.LAST_NAME] = value

    def get_users_profile_age(self, user_id: int) -> int:
        if user_id == self.__id:
            return self.__profile[constants.ProfileItemsIds.AGE]
        else:
            return self.USERS_LIST[user_id].age

    def set_users_profile_age(self, user_id: int, value: int) -> None:
        self.__profile[constants.ProfileItemsIds.AGE] = value

    def get_users_profile_spoken_languages(self, user_id: int) -> List[constants.SpokenLanguages]:
        if user_id == self.__id:
            return self.__profile[constants.ProfileItemsIds.SPOKEN_LANGUAGES]
        else:
            return self.USERS_LIST[user_id].spoken_languages

    def append_to_users_profile_spoken_languages(self, user_id: int, value: constants.SpokenLanguages) -> None:
        if self.__profile[constants.ProfileItemsIds.SPOKEN_LANGUAGES] is None:
            self.__profile[constants.ProfileItemsIds.SPOKEN_LANGUAGES] = {value}
        else:
            self.__profile[constants.ProfileItemsIds.SPOKEN_LANGUAGES].add(value)

    def set_users_profile_spoken_languages_null(self, user_id: int) -> None:
        self.__profile[constants.ProfileItemsIds.SPOKEN_LANGUAGES] = None

    def get_users_profile_programming_languages(self, user_id: int) -> List[constants.ProgrammingLanguages]:
        if user_id == self.__id:
            return self.__profile[constants.ProfileItemsIds.PROGRAMMING_LANGUAGES]
        else:
            return self.USERS_LIST[user_id].programming_languages

    def append_to_users_profile_programming_languages(self, user_id: int,
                                                      value: constants.ProgrammingLanguages) -> None:
        if self.__profile[constants.ProfileItemsIds.PROGRAMMING_LANGUAGES] is None:
            self.__profile[constants.ProfileItemsIds.PROGRAMMING_LANGUAGES] = {value}
        else:
            self.__profile[constants.ProfileItemsIds.PROGRAMMING_LANGUAGES].add(value)

    def set_users_profile_programming_languages_null(self, user_id: int) -> None:
        self.__profile[constants.ProfileItemsIds.PROGRAMMING_LANGUAGES] = None

    def get_users_profile_interests(self, user_id: int) -> List[constants.Interests]:
        if user_id == self.__id:
            return self.__profile[constants.ProfileItemsIds.INTERESTS]
        else:
            return self.USERS_LIST[user_id].interests

    def append_to_users_profile_interests(self, user_id: int, value: constants.Interests) -> None:
        if self.__profile[constants.ProfileItemsIds.INTERESTS] is None:
            self.__profile[constants.ProfileItemsIds.INTERESTS] = {value}
        else:
            self.__profile[constants.ProfileItemsIds.INTERESTS].add(value)

    def set_users_profile_interests_null(self, user_id: int) -> None:
        self.__profile[constants.ProfileItemsIds.INTERESTS] = None

    # SEARCH PARAMETERS

    def are_search_parameters_filled(self, user_id: int) -> bool:
        return self.__are_search_parameters_filled

    def set_search_parameters_filled(self, user_id: int) -> None:
        self.__are_search_parameters_filled = True

    def get_users_search_parameter_item_id(self, user_id: int) -> constants.SearchParametersItemsIds:
        return self.__navigation[NavigationItems.SEARCH_PARAMETER_ITEM_ID]

    def set_users_search_parameters_item_id(self, user_id: int,
                                            new_search_parameter_item_id: constants.SearchParametersItemsIds) -> None:
        self.__navigation[NavigationItems.SEARCH_PARAMETER_ITEM_ID] = new_search_parameter_item_id

    def get_users_search_parameters_age_groups(self, user_id: int) -> List[constants.AgeGroups]:
        return self.__search_parameters[constants.SearchParametersItemsIds.AGE_GROUP]

    def append_to_users_search_parameters_age_groups(self, user_id: int, value: constants.AgeGroups) -> None:
        if self.__search_parameters[constants.SearchParametersItemsIds.AGE_GROUP] is None:
            self.__search_parameters[constants.SearchParametersItemsIds.AGE_GROUP] = {value}
        else:
            self.__search_parameters[constants.SearchParametersItemsIds.AGE_GROUP].add(value)

    def set_users_profile_search_parameters_age_groups_null(self, user_id: int) -> None:
        self.__search_parameters[constants.SearchParametersItemsIds.AGE_GROUP] = None

    def get_users_search_parameters_spoken_languages(self, user_id: int) -> List[constants.SpokenLanguages]:
        return self.__search_parameters[constants.SearchParametersItemsIds.SPOKEN_LANGUAGES]

    def append_to_users_search_parameters_spoken_languages(self, user_id: int,
                                                           value: constants.SpokenLanguages) -> None:
        if self.__search_parameters[constants.SearchParametersItemsIds.SPOKEN_LANGUAGES] is None:
            self.__search_parameters[constants.SearchParametersItemsIds.SPOKEN_LANGUAGES] = {value}
        else:
            self.__search_parameters[constants.SearchParametersItemsIds.SPOKEN_LANGUAGES].add(value)

    def set_users_profile_search_parameters_spoken_languages_null(self, user_id: int) -> None:
        self.__search_parameters[constants.SearchParametersItemsIds.SPOKEN_LANGUAGES] = None

    def get_users_search_parameters_programming_languages(self, user_id: int) -> List[constants.ProgrammingLanguages]:
        return self.__search_parameters[constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES]

    def append_to_users_search_parameters_programming_languages(self, user_id: int,
                                                                value: constants.ProgrammingLanguages) -> None:
        if self.__search_parameters[constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES] is None:
            self.__search_parameters[constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES] = {value}
        else:
            self.__search_parameters[constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES].add(value)

    def set_users_profile_search_parameters_programming_languages_null(self, user_id: int) -> None:
        self.__search_parameters[constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES] = None

    def get_users_search_parameters_interests(self, user_id: int) -> List[constants.Interests]:
        return self.__search_parameters[constants.SearchParametersItemsIds.INTERESTS]

    def append_to_users_search_parameters_interests(self, user_id: int, value: constants.Interests) -> None:
        if self.__search_parameters[constants.SearchParametersItemsIds.INTERESTS] is None:
            self.__search_parameters[constants.SearchParametersItemsIds.INTERESTS] = {value}
        else:
            self.__search_parameters[constants.SearchParametersItemsIds.INTERESTS].add(value)

    def set_users_profile_search_parameters_interests_null(self, user_id: int) -> None:
        self.__search_parameters[constants.SearchParametersItemsIds.INTERESTS] = None

    # OTHER USER DATA

    def get_users_last_shown_profile_id(self, user_id: int) -> Optional[int]:
        return self.__last_profile_id

    def set_users_last_shown_profile_id(self, user_id: int, candidate_id: int) -> None:
        self.__last_profile_id = candidate_id

    def get_users_telegram_login_by_id(self, user_id: int) -> str:
        if user_id == self.__id:
            return self.__telegram_login
        else:
            return self.USERS_LIST[user_id].telegram_login

    def get_number_of_likes(self, user_id: int) -> int:
        return self.__number_of_likes

    def inc_number_of_likes(self, user_id: int) -> None:
        self.__number_of_likes += 1

    def have_subscription(self, user_id: int) -> bool:
        return self.__subscription

    def activate_subscription(self, user_id: int) -> None:
        self.__subscription = True

    def deactivate_subscription(self, user_id: int) -> None:
        self.__subscription = False

    def add_candidate(self, user_id: int, candidate_id: int) -> None:
        self.__potential_relationships.append([user_id, candidate_id, False])

    def get_not_viewed_candidates(self, user_id: int) -> Optional[List[int]]:
        return [pr[1] for pr in self.__potential_relationships if not pr[2]]

    def mark_profile_as_viewed(self, user_id: int, candidate_id: int) -> None:
        for i in range(len(self.__potential_relationships)):
            if self.__potential_relationships[i][1] == candidate_id:
                self.__potential_relationships[i][2] = True

    def get_all_users(self) -> List[int]:
        return [user.id for user in self.USERS_LIST]

    def is_profile_viewed(self, user_id: int, candidate_id: int) -> bool:
        for i in range(len(self.__potential_relationships)):
            if self.__potential_relationships[i][1] == candidate_id:
                return self.__potential_relationships[i][2]
        return False


class NavigationItems(enum.Enum):
    """
    Items for table 'navigation' which contains info about users position in menu's tree
    """
    MENU_ID = enum.auto()
    REGISTRATION_ITEM_ID = enum.auto()
    SEARCH_PARAMETER_ITEM_ID = enum.auto()


class PotentialRelationshipItems(enum.Enum):
    """
    Items for table 'potential_relationship' which contains info about profiles that can be shown to the user
    """
    SENDER_ACCOUNT_ID = enum.auto()
    REQUESTED_ACCOUNT_ID = enum.auto()
    IS_VIEWED = enum.auto()
