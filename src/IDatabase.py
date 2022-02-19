from abc import ABC, abstractmethod
from typing import Optional, List

import constants


class IDatabase(ABC):
    """
    Interface for classes working with database
    """

    # REGISTRATION AND PROFILE

    @abstractmethod
    def is_in_database(self, user_id: int) -> bool:
        """
        :param user_id: Telegram's id of user we work with
        :return: is user with user_id in database
        """
        pass

    @abstractmethod
    def initial_user_setup(self, user_id: int) -> None:
        """
        :param user_id: Telegram's id of user we work with
        """
        pass

    @abstractmethod
    def set_users_telegram_login(self, user_id: int, login: str) -> None:
        """
        :param user_id: Telegram's id of user we work with
        :param login: user's telegram login
        """
        pass

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
    def get_users_profile_first_name(self, user_id: int) -> Optional[str]:
        """
        :param user_id: Telegram's id of user we work with
        :return: value of "First name" field in user's profile
        """
        pass

    @abstractmethod
    def set_users_profile_first_name(self, user_id: int, value: Optional[str]) -> None:
        """
        Set value of "First name" field in user's profile
        :param user_id: Telegram's id of user we work with
        :param value: new value of "First name" field in user's profile
        """
        pass

    @abstractmethod
    def get_users_profile_last_name(self, user_id: int) -> Optional[str]:
        """
        :param user_id: Telegram's id of user we work with
        :return: value of "Last name" field in user's profile
        """
        pass

    @abstractmethod
    def set_users_profile_last_name(self, user_id: int, value: Optional[str]) -> None:
        """
        Set value of "Last name" field in user's profile
        :param user_id: Telegram's id of user we work with
        :param value: new value of "Last name" field in user's profile
        """
        pass

    @abstractmethod
    def get_users_profile_age(self, user_id: int) -> Optional[int]:
        """
        :param user_id: Telegram's id of user we work with
        :return: value of "Age" field in user's profile
        """
        pass

    @abstractmethod
    def set_users_profile_age(self, user_id: int, value: Optional[int]) -> None:
        """
        Set value of "Age" field in user's profile
        :param user_id: Telegram's id of user we work with
        :param value: new value of "Age" field in user's profile
        """
        pass

    @abstractmethod
    def get_users_profile_spoken_languages(self, user_id: int) -> List[constants.SpokenLanguages]:
        """
        :param user_id: Telegram's id of user we work with
        :return: value of "Spoken languages" field in user's profile
        """
        pass

    @abstractmethod
    def append_to_users_profile_spoken_languages(self, user_id: int, value: constants.SpokenLanguages) -> None:
        """
        Append value to "Spoken languages" field in user's profile
        :param user_id: Telegram's id of user we work with
        :param value: appended value
        """
        pass

    @abstractmethod
    def remove_from_users_profile_spoken_languages(self, user_id: int,
                                                   value: constants.SpokenLanguages) -> None:
        """
        Remove value from "Spoken languages" field in user's profile
        :param user_id: Telegram's id of user we work with
        :param value: removed value
        """
        pass

    @abstractmethod
    def set_users_profile_spoken_languages_null(self, user_id: int) -> None:
        """
        Set "Spoken languages" field in user's profile = Null
        :param user_id: Telegram's id of user we work with
        """
        pass

    @abstractmethod
    def get_users_profile_programming_languages(self, user_id: int) -> List[constants.ProgrammingLanguages]:
        """
        :param user_id: Telegram's id of user we work with
        :return: value of "Programming languages" field in user's profile
        """
        pass

    @abstractmethod
    def append_to_users_profile_programming_languages(self, user_id: int,
                                                      value: constants.ProgrammingLanguages) -> None:
        """
        Append value to "Programming languages" field in user's profile
        :param user_id: Telegram's id of user we work with
        :param value: appended value
        """
        pass

    @abstractmethod
    def remove_from_users_profile_programming_languages(self, user_id: int,
                                                        value: constants.ProgrammingLanguages) -> None:
        """
        Remove value from "Programming languages" field in user's profile
        :param user_id: Telegram's id of user we work with
        :param value: removed value
        """
        pass

    @abstractmethod
    def set_users_profile_programming_languages_null(self, user_id: int) -> None:
        """
        Set "Programming languages" field in user's profile = Null
        :param user_id: Telegram's id of user we work with
        """
        pass

    @abstractmethod
    def get_users_profile_interests(self, user_id: int) -> List[constants.Interests]:
        """
        :param user_id: Telegram's id of user we work with
        :return: value of "Interests" field in user's profile
        """
        pass

    @abstractmethod
    def append_to_users_profile_interests(self, user_id: int, value: constants.Interests) -> None:
        """
        Append value to "Interests" field in user's profile
        :param user_id: Telegram's id of user we work with
        :param value: appended value
        """
        pass

    @abstractmethod
    def remove_from_users_profile_interests(self, user_id: int,
                                            value: constants.Interests) -> None:
        """
        Remove value from "Interests" field in user's profile
        :param user_id: Telegram's id of user we work with
        :param value: removed value
        """
        pass

    @abstractmethod
    def set_users_profile_interests_null(self, user_id: int) -> None:
        """
        Set "Interests" field in user's profile = Null
        :param user_id: Telegram's id of user we work with
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
    def set_users_search_parameters_item_id(self, user_id: int,
                                            new_search_parameter_item_id: constants.SearchParametersItemsIds) -> None:
        """
        :param user_id: Telegram's id of user we work with
        :param new_search_parameter_item_id: new value of "search_parameter_item_id" field
            (id of current search parameter's item during the filling process) for user
        """
        pass

    @abstractmethod
    def get_users_search_parameters_age_groups(self, user_id: int) -> List[constants.AgeGroups]:
        """
        :param user_id: Telegram's id of user we work with
        :return: value of "Age groups" field in user's search parameters
        """
        pass

    @abstractmethod
    def append_to_users_search_parameters_age_groups(self, user_id: int, value: constants.AgeGroups) -> None:
        """
        Append value to "Age groups" field in user's search parameters
        :param user_id: Telegram's id of user we work with
        :param value: appended value
        """
        pass

    @abstractmethod
    def remove_from_users_search_parameters_age_groups(self, user_id: int,
                                                       value: constants.AgeGroups) -> None:
        """
        Remove value from "Age groups" field in user's search parameters
        :param user_id: Telegram's id of user we work with
        :param value: removed value
        """
        pass

    @abstractmethod
    def set_users_profile_search_parameters_age_groups_null(self, user_id: int) -> None:
        """
        Set "Age groups" field in user's search parameters = Null
        :param user_id: Telegram's id of user we work with
        """
        pass

    @abstractmethod
    def get_users_search_parameters_spoken_languages(self, user_id: int) -> List[constants.SpokenLanguages]:
        """
        :param user_id: Telegram's id of user we work with
        :return: value of "Spoken languages" field in user's search parameters
        """
        pass

    @abstractmethod
    def append_to_users_search_parameters_spoken_languages(self, user_id: int,
                                                           value: constants.SpokenLanguages) -> None:
        """
        Append value to "Spoken languages" field in user's search parameters
        :param user_id: Telegram's id of user we work with
        :param value: appended value
        """
        pass

    @abstractmethod
    def remove_from_users_search_parameters_spoken_languages(self, user_id: int,
                                                             value: constants.SpokenLanguages) -> None:
        """
        Remove value from "Spoken languages" field in user's search parameters
        :param user_id: Telegram's id of user we work with
        :param value: removed value
        """
        pass

    @abstractmethod
    def set_users_profile_search_parameters_spoken_languages_null(self, user_id: int) -> None:
        """
        Set "Spoken Languages" field in user's search parameters = Null
        :param user_id: Telegram's id of user we work with
        """
        pass

    @abstractmethod
    def get_users_search_parameters_programming_languages(self, user_id: int) -> List[constants.ProgrammingLanguages]:
        """
        :param user_id: Telegram's id of user we work with
        :return: value of "Programming languages" field in user's search parameters
        """
        pass

    @abstractmethod
    def append_to_users_search_parameters_programming_languages(self, user_id: int,
                                                                value: constants.ProgrammingLanguages) -> None:
        """
        Append value to "Programming languages" field in user's search parameters
        :param user_id: Telegram's id of user we work with
        :param value: appended value
        """
        pass

    @abstractmethod
    def remove_from_users_search_parameters_programming_languages(self, user_id: int,
                                                                  value: constants.ProgrammingLanguages) -> None:
        """
        Remove value from "Programming languages" field in user's search parameters
        :param user_id: Telegram's id of user we work with
        :param value: removed value
        """
        pass

    @abstractmethod
    def set_users_profile_search_parameters_programming_languages_null(self, user_id: int) -> None:
        """
        Set "Programming Languages" field in user's search parameters = Null
        :param user_id: Telegram's id of user we work with
        """
        pass

    @abstractmethod
    def get_users_search_parameters_interests(self, user_id: int) -> List[constants.Interests]:
        """
        :param user_id: Telegram's id of user we work with
        :return: value of "Interests" field in user's search parameters
        """
        pass

    @abstractmethod
    def append_to_users_search_parameters_interests(self, user_id: int, value: constants.Interests) -> None:
        """
        Append value to "Interests" field in user's search parameters
        :param user_id: Telegram's id of user we work with
        :param value: appended value
        """
        pass

    @abstractmethod
    def remove_from_users_search_parameters_interests(self, user_id: int,
                                                      value: constants.Interests) -> None:
        """
        Remove value from "Interests" field in user's search parameters
        :param user_id: Telegram's id of user we work with
        :param value: removed value
        """
        pass

    @abstractmethod
    def set_users_profile_search_parameters_interests_null(self, user_id: int) -> None:
        """
        Set "Interests" field in user's search parameters = Null
        :param user_id: Telegram's id of user we work with
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

    @abstractmethod
    def have_subscription(self, user_id: int) -> bool:
        """
        :return: does the user have a subscription
        """
        pass

    @abstractmethod
    def activate_subscription(self, user_id: int) -> None:
        """
        Mark that the user have subscription
        """
        pass

    @abstractmethod
    def deactivate_subscription(self, user_id: int) -> None:
        """
        Mark that the user does not have a subscription
        """
        pass

    @abstractmethod
    def add_candidate(self, user_id: int, candidate_id: int) -> None:
        """
        Add candidate to potential profiles
        :param user_id: Telegram's id of user we work with
        :param candidate_id: id of the candidate being added
        """
        pass

    @abstractmethod
    def get_not_viewed_candidates(self, user_id: int) -> Optional[List[int]]:
        """
        :param user_id: Telegram's id of user we work with
        :return: list of not viewed by user (with user_id) profiles
        """
        pass

    @abstractmethod
    def mark_profile_as_viewed(self, user_id: int, candidate_id: int) -> None:
        """
        :param user_id: Telegram's id of user we work with
        :param candidate_id: id of the candidate being marked
        """
        pass

    @abstractmethod
    def get_all_users(self) -> List[int]:
        """
        :return: list with all user's ids
        """
        pass

    @abstractmethod
    def is_profile_in_candidates_list(self, user_id: int, candidate_id: int) -> bool:
        """
        :return: is pair user_id - candidate_id is in potentials_profiles
        """
        pass
