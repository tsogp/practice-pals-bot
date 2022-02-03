import enum
from typing import Optional

from IDatabase import IDatabase

import constants


class FakeDatabase(IDatabase):
    """
    Fake database for development (do not use in production)"
    """

    def __init__(self):
        self.__id: int = 1
        self.__telegram_login: str = "None"
        self.__telegram_id: int = 0
        self.__is_registered: bool = False
        self.__are_search_parameters_filled = False

        self.__navigation: dict = {
            NavigationItems.MENU_ID: constants.MenuIds.NULL,
            NavigationItems.REGISTRATION_ITEM_ID: constants.ProfileItemsIds.NULL,
            NavigationItems.SEARCH_PARAMETER_ITEM_ID: constants.SearchParametersItemsIds.NULL
        }

        self.__profile: dict = {
            constants.ProfileItemsIds.FIRST_NAME: None,
            constants.ProfileItemsIds.LAST_NAME: None,
            constants.ProfileItemsIds.AGE: None,
            constants.ProfileItemsIds.SPOKEN_LANGUAGES: set(),
            constants.ProfileItemsIds.PROGRAMMING_LANGUAGES: set(),
            constants.ProfileItemsIds.INTERESTS: set()
        }

        self.__search_parameters: dict = {
            constants.SearchParametersItemsIds.AGE_GROUP: set(),
            constants.SearchParametersItemsIds.SPOKEN_LANGUAGES: set(),
            constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES: set(),
            constants.SearchParametersItemsIds.INTERESTS: set()
        }

        self.__potential_relationship: dict = {
            PotentialRelationshipItems.SENDER_ACCOUNT_ID: None,
            PotentialRelationshipItems.REQUESTED_ACCOUNT_ID: None,
            PotentialRelationshipItems.IS_VIEWED: None,
        }

        self.__number_of_likes: int = 0
        self.__last_profile_id: Optional[int] = None

    # REGISTRATION AND PROFILE

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

    def get_users_profile_item(self, user_id: int, item: constants.ProfileItemsIds) -> Optional[str]:
        if self.__profile[item] is None:
            return None
        if item in (constants.ProfileItemsIds.SPOKEN_LANGUAGES, constants.ProfileItemsIds.PROGRAMMING_LANGUAGES,
                    constants.ProfileItemsIds.INTERESTS):
            return ", ".join(self.__profile[item])
        else:
            return self.__profile[item]

    def set_users_profile_item(self, user_id: int, item: constants.ProfileItemsIds, value: Optional[str]) -> None:
        self.__profile[item] = value

    def append_to_users_profile_item(self, user_id: int, item: constants.ProfileItemsIds, value: str) -> None:
        self.__profile[item].add(value)

    # SEARCH PARAMETERS

    def are_search_parameters_filled(self, user_id: int) -> bool:
        return self.__are_search_parameters_filled

    def set_search_parameters_filled(self, user_id: int) -> None:
        self.__are_search_parameters_filled = True

    def get_users_search_parameter_item_id(self, user_id: int) -> constants.SearchParametersItemsIds:
        return self.__navigation[NavigationItems.SEARCH_PARAMETER_ITEM_ID]

    def set_users_search_parameter_item_id(self, user_id: int,
                                           new_search_parameter_item_id: constants.SearchParametersItemsIds) -> None:
        self.__navigation[NavigationItems.SEARCH_PARAMETER_ITEM_ID] = new_search_parameter_item_id

    def get_users_search_parameter_item(self, user_id: int, item: constants.SearchParametersItemsIds) -> Optional[str]:
        if self.__search_parameters[item] is None:
            return None
        return ", ".join(self.__search_parameters[item])

    def append_to_users_search_parameter_item(self, user_id: int, item: constants.SearchParametersItemsIds,
                                              value: Optional[str]) -> None:
        self.__search_parameters[item].add(value)

    # OTHER USER DATA

    def get_users_last_shown_profile_id(self, user_id: int) -> Optional[int]:
        return self.__last_profile_id

    def set_users_last_shown_profile_id(self, user_id: int, candidate_id: int) -> None:
        self.__last_profile_id = candidate_id

    def get_users_telegram_login_by_id(self, user_id: int) -> str:
        return self.__telegram_login

    def get_number_of_likes(self, user_id: int) -> int:
        return self.__number_of_likes

    def inc_number_of_likes(self, user_id: int) -> None:
        self.__number_of_likes += 1


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
