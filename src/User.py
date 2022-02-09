from IDatabase import IDatabase
import constants
import phrases_ru as phrases
from typing import Optional, List


class User:
    __DATABASE: Optional[IDatabase] = None  # Bot's database object

    @classmethod
    def set_database(cls, database: IDatabase) -> None:
        """
        Set bot's database object.
        MUST BE CALLED BEFORE CREATING OBJECTS!
        """
        cls.__DATABASE = database

    def __init__(self, user_id: int):
        self.__id = user_id
        self.__menu_id = User.__DATABASE.get_users_menu_id(self.__id)
        self.__registration_item_id = User.__DATABASE.get_users_registration_item_id(self.__id)
        self.__search_parameter_item_id = User.__DATABASE.get_users_search_parameter_item_id(self.__id)

    def is_in_menu(self, menu_id: constants.MenuIds) -> bool:
        """
        Check, is user in menu with menu_id
        """
        return self.__menu_id == menu_id

    def is_in_registration_item(self, profile_item_id: constants.ProfileItemsIds) -> bool:
        """
        Check, is user filling registration_item with profile_item_id
        """
        check_menu_id = self.__menu_id == constants.MenuIds.REGISTRATION_MENU
        check_registration_item_id = self.__registration_item_id == profile_item_id
        return check_menu_id and check_registration_item_id

    def is_in_search_parameters_item(self, search_parameters_item_id: constants.SearchParametersItemsIds) -> bool:
        """
        Check, is user filling search parameter with search_parameters_item_id
        """
        check_menu_id = self.__menu_id == constants.MenuIds.SEARCH_PARAMETERS_MENU
        check_search_parameter_item_id = self.__search_parameter_item_id == search_parameters_item_id
        return check_menu_id and check_search_parameter_item_id

    def is_like_acceptable(self) -> bool:
        if User.__DATABASE.have_subscription(self.__id):
            return True
        else:
            return User.__DATABASE.get_number_of_likes(self.__id) < constants.MAXIMUM_NUMBER_OF_LIKES

    def get_profile(self) -> str:
        """
        :return: list of profile items and it's values in string with markdown
        """
        profile = ""
        profile += self.__get_profile_first_name()
        profile += self.__get_profile_last_name()
        profile += self.__get_profile_age()
        profile += self.__get_profile_spoken_languages()
        profile += self.__get_profile_programming_languages()
        profile += self.__get_profile_interests()
        return profile

    def __get_str_from_list(self, raw_value: Optional[List[constants.PossibleAnswers]]):
        if raw_value is None:
            values = "_" + phrases.item_is_not_specified + "_"
        else:
            values = ""
            for v in raw_value:
                values += (v.value + " ")
        return values

    def __get_profile_first_name(self) -> str:
        title = f"*{phrases.profile_items[constants.ProfileItemsIds.FIRST_NAME]}:* "
        raw_value = User.__DATABASE.get_users_profile_first_name(self.__id)
        value = raw_value if raw_value is not None else ("_" + phrases.item_is_not_specified + "_")
        return title + value + "\n"

    def __get_profile_last_name(self) -> str:
        title = f"*{phrases.profile_items[constants.ProfileItemsIds.LAST_NAME]}:* "
        raw_value = User.__DATABASE.get_users_profile_last_name(self.__id)
        value = raw_value if raw_value is not None else ("_" + phrases.item_is_not_specified + "_")
        return title + value + "\n"

    def __get_profile_age(self) -> str:
        title = f"*{phrases.profile_items[constants.ProfileItemsIds.AGE]}:* "
        raw_value = User.__DATABASE.get_users_profile_age(self.__id)
        value = str(raw_value) if raw_value is not None else ("_" + phrases.item_is_not_specified + "_")
        return title + value + "\n"

    def __get_profile_spoken_languages(self) -> str:
        title = f"*{phrases.profile_items[constants.ProfileItemsIds.SPOKEN_LANGUAGES]}:* "
        raw_value = User.__DATABASE.get_users_profile_spoken_languages(self.__id)
        values = self.__get_str_from_list(raw_value)
        return title + values + "\n"

    def __get_profile_programming_languages(self) -> str:
        title = f"*{phrases.profile_items[constants.ProfileItemsIds.PROGRAMMING_LANGUAGES]}:* "
        raw_value = User.__DATABASE.get_users_profile_programming_languages(self.__id)
        values = self.__get_str_from_list(raw_value)
        return title + values + "\n"

    def __get_profile_interests(self) -> str:
        title = f"*{phrases.profile_items[constants.ProfileItemsIds.INTERESTS]}:* "
        raw_value = User.__DATABASE.get_users_profile_interests(self.__id)
        values = self.__get_str_from_list(raw_value)
        return title + values + "\n"

    def get_search_parameters(self) -> str:
        """
        :return: list of profile items and it's values in string with markdown
        """
        search_parameters = ""
        search_parameters += self.__get_search_parameters_age_groups()
        search_parameters += self.__get_search_parameters_spoken_languages()
        search_parameters += self.__get_search_parameters_programming_languages()
        search_parameters += self.__get_search_parameters_interests()

        return search_parameters

    def __get_search_parameters_age_groups(self) -> str:
        title = f"*{phrases.search_parameters_items[constants.SearchParametersItemsIds.AGE_GROUP]}:* "
        raw_value = User.__DATABASE.get_users_search_parameters_age_groups(self.__id)
        values = self.__get_str_from_list(raw_value)
        return title + values + "\n"

    def __get_search_parameters_spoken_languages(self) -> str:
        title = f"*{phrases.search_parameters_items[constants.SearchParametersItemsIds.SPOKEN_LANGUAGES]}:* "
        raw_value = User.__DATABASE.get_users_search_parameters_spoken_languages(self.__id)
        values = self.__get_str_from_list(raw_value)
        return title + values + "\n"

    def __get_search_parameters_programming_languages(self) -> str:
        title = f"*{phrases.search_parameters_items[constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES]}:* "
        raw_value = User.__DATABASE.get_users_search_parameters_programming_languages(self.__id)
        values = self.__get_str_from_list(raw_value)
        return title + values + "\n"

    def __get_search_parameters_interests(self) -> str:
        title = f"*{phrases.search_parameters_items[constants.SearchParametersItemsIds.INTERESTS]}:* "
        raw_value = User.__DATABASE.get_users_search_parameters_interests(self.__id)
        values = self.__get_str_from_list(raw_value)
        return title + values + "\n"

    def create_candidates_list(self) -> None:
        spoken_languages = self.__DATABASE.get_users_search_parameters_spoken_languages(self.__id)
        programming_languages = self.__DATABASE.get_users_search_parameters_programming_languages(self.__id)
        interests = self.__DATABASE.get_users_search_parameters_interests(self.__id)
        candidates_ids = self.__DATABASE.get_users_by_parameters(spoken_languages, programming_languages, interests)

        for candidate_id in candidates_ids:
            self.__DATABASE.add_candidate(self.__id, candidate_id)

    def get_candidate_id(self) -> Optional[int]:
        candidates = self.__DATABASE.get_not_viewed_candidates(self.__id)
        if not candidates:
            return None
        return candidates[0]
