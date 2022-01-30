from abc import ABC, abstractmethod
from typing import Optional

import constants


class IDatabase(ABC):
    """
    Interface for classes working with database
    """

    # REGISTRATION AND PROFILE

    @abstractmethod
    def is_registered(self, user_id: int) -> bool:
        """
        Check, is user registered
        :param user_id: Telegram's id of user we work with
        :return: if user in database, returns value of "is_registered" field, else returns False
        """
        pass

    @abstractmethod
    def register_user(self, user_id: int) -> None:
        """
        Mark the user as registered
        :param user_id: Telegram's id of user we work with
        """
        pass

    @abstractmethod
    def get_users_menu_id(self, user_id: int) -> constants.MenuIds:
        """
        :param user_id: Telegram's id of user we work with
        :return: value of "menu_id" field (id of current active menu) for user
        """
        pass

    @abstractmethod
    def set_users_menu_id(self, user_id: int, new_menu_id: constants.MenuIds) -> None:
        """
        Set id of new active menu for user
        :param user_id: Telegram's id of user we work with
        :param new_menu_id: new value of "menu_id" field (id of current active menu) for user
        """
        pass

    @abstractmethod
    def get_users_registration_item_id(self, user_id: int) -> constants.ProfileItemsIds:
        """
        :param user_id: Telegram's id of user we work with
        :return: value of "registration_item_id" field
            (id of current profile item during the registration process) for user
        """
        pass

    @abstractmethod
    def set_users_registration_item_id(self, user_id: int, new_registration_item_id: constants.ProfileItemsIds) -> None:
        """
        :param user_id: Telegram's id of user we work with
        :param new_registration_item_id: new value of "registration_item_id" field
            (id of current profile item during the registration process) for user
        """
        pass

    @abstractmethod
    def get_users_profile_item(self, user_id: int, item: constants.ProfileItemsIds) -> Optional[str]:
        """
        Get value of item from user's profile
        :param user_id: Telegram's id of user we work with
        :param item: id of profile's item
        :return: value of profile's item
        """
        pass

    @abstractmethod
    def set_users_profile_item(self, user_id: int, item: constants.ProfileItemsIds, value: Optional[str]) -> None:
        """
        Set new value of item from user's profile
        :param user_id: Telegram's id of user we work with
        :param item: id of profile's item which needs to be changed
        :param value: new value for item
        """
        pass

    @abstractmethod
    def append_to_users_profile_item(self, user_id: int, item: constants.ProfileItemsIds, value: str) -> None:
        """
        Append some value into user's profile item
        :param user_id: Telegram's id of user we work with
        :param item: id of profile's item which needs to be changed
        :param value: value to be added
        """
        pass

    # SEARCH PARAMETERS

    @abstractmethod
    def are_search_parameters_filled(self, user_id: int) -> bool:
        """
        :param user_id: Telegram's id of user we work with
        :return: value of "are_search_parameters_filled" field (has the user filled in the search parameters) for user
        """
        pass

    @abstractmethod
    def set_search_parameters_filled(self, user_id: int) -> None:
        """
        Mark the user as having filled in the search parameters
        :param user_id:Telegram's id of user we work with
        """
        pass

    @abstractmethod
    def get_users_search_parameter_item_id(self, user_id: int) -> constants.SearchParametersItemsIds:
        """
        :param user_id: Telegram's id of user we work with
        :return: value of "users_search_parameter_item_id" field
            (id of current search parameters item during the filling process) for user
        """
        pass

    @abstractmethod
    def set_users_search_parameter_item_id(self, user_id: int,
                                           new_search_parameter_item_id: constants.SearchParametersItemsIds) -> None:
        """
        :param user_id: Telegram's id of user we work with
        :param new_search_parameter_item_id: new value of "search_parameter_item_id" field
            (id of current search parameter's item during the filling process) for user
        """
        pass

    @abstractmethod
    def get_users_search_parameter_item(self, user_id: int, item: constants.SearchParametersItemsIds) -> Optional[str]:
        """
        Get value of item from user's search parameters
        :param user_id: Telegram's id of user we work with
        :param item: id of search parameters item
        :return: value of search parameters item
        """
        pass

    @abstractmethod
    def append_to_users_search_parameter_item(self, user_id: int, item: constants.SearchParametersItemsIds,
                                              value: Optional[str]) -> None:
        """
        Append some value into user's search parameters item
        :param user_id: Telegram's id of user we work with
        :param item: id of search parameters item which needs to be changed
        :param value: value to be added
        """
        pass

    # OTHER USER DATA

    @abstractmethod
    def get_users_last_shown_profile_id(self, user_id: int) -> Optional[int]:
        """
        :param user_id: Telegram's id of user we work with
        :return: value of "last_shown_profile_id" field (id of the last profile shown to the user) for user
        """
        pass

    @abstractmethod
    def set_users_last_shown_profile_id(self, user_id: int, candidate_id: Optional[int]) -> None:
        """
        :param user_id: Telegram's id of user we work with
        :param candidate_id: id of the last profile shown to the user
        """
        pass

    @abstractmethod
    def get_users_telegram_login_by_id(self, user_id: int) -> str:
        """
        :param user_id: Telegram's id of user we work with
        :return: user's Telegram login
        """
        pass

    @abstractmethod
    def get_number_of_likes(self, user_id: int) -> int:
        """
        :param user_id: Telegram's id of user we work with
        :return: value of "number_of_likes" field
        """
        pass

    @abstractmethod
    def inc_number_of_likes(self, user_id: int) -> None:
        """
        Increase value of "number_of_likes" field by 1
        :param user_id: Telegram's id of user we work with
        """
        pass
