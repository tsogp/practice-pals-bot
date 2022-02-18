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

    def is_in_menu(self, menu_id: constants.MenuIds) -> bool:
        """
        Check, is user in menu with menu_id
        """
        user_menu_id = User.__DATABASE.get_users_menu_id(self.__id)
        return user_menu_id == menu_id

    def is_in_registration_item(self, profile_item_id: constants.ProfileItemsIds) -> bool:
        """
        Check, is user filling registration_item with profile_item_id
        """
        menu_id = User.__DATABASE.get_users_menu_id(self.__id)
        check_menu_id = menu_id == constants.MenuIds.REGISTRATION_MENU

        __registration_item_id = User.__DATABASE.get_users_registration_item_id(self.__id)
        check_registration_item_id = __registration_item_id == profile_item_id

        return check_menu_id and check_registration_item_id

    def is_in_search_parameters_item(self, search_parameters_item_id: constants.SearchParametersItemsIds) -> bool:
        """
        Check, is user filling search parameter with search_parameters_item_id
        """
        menu_id = User.__DATABASE.get_users_menu_id(self.__id)
        check_menu_id = menu_id == constants.MenuIds.SEARCH_PARAMETERS_MENU

        __search_parameter_item_id = User.__DATABASE.get_users_search_parameter_item_id(self.__id)
        check_search_parameter_item_id = __search_parameter_item_id == search_parameters_item_id

        return check_menu_id and check_search_parameter_item_id

    def is_like_acceptable(self) -> bool:
        """
        Check if the user can put a like
        """
        if User.__DATABASE.have_subscription(self.__id):
            return True
        else:
            return User.__DATABASE.get_number_of_likes(self.__id) < constants.MAXIMUM_NUMBER_OF_LIKES

    # GET PROFILE

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

    @staticmethod
    def __get_str_from_list(raw_value: Optional[List[constants.Items]], mode: int):
        if raw_value is None:
            values = "_" + (phrases.item_is_not_specified if mode == 0 else phrases.does_not_matter_without_emoji) + "_"
        else:
            values = ""
            for i in range(len(raw_value) - 1):
                try:
                    item_str = phrases.values_of_enums_constants[raw_value[i]]
                except KeyError:
                    item_str = raw_value[i].value
                    constants.logger.error(f"Can't find value for {raw_value[i]} in dictionary")
                values += (item_str + ", ")

            try:
                item_str = phrases.values_of_enums_constants[raw_value[-1]]
            except KeyError:
                item_str = raw_value[-1].value
                constants.logger.error(f"Can't find value for {raw_value[-1]} in dictionary")
            values += item_str

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
        values = User.__get_str_from_list(raw_value, mode=0)
        return title + values + "\n"

    def __get_profile_programming_languages(self) -> str:
        title = f"*{phrases.profile_items[constants.ProfileItemsIds.PROGRAMMING_LANGUAGES]}:* "
        raw_value = User.__DATABASE.get_users_profile_programming_languages(self.__id)
        values = User.__get_str_from_list(raw_value, mode=0)
        return title + values + "\n"

    def __get_profile_interests(self) -> str:
        title = f"*{phrases.profile_items[constants.ProfileItemsIds.INTERESTS]}:* "
        raw_value = User.__DATABASE.get_users_profile_interests(self.__id)
        values = User.__get_str_from_list(raw_value, mode=0)
        return title + values + "\n"

    # GET PROFILE

    # GET SEARCH PARAMETERS
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
        values = User.__get_str_from_list(raw_value, mode=1)
        return title + values + "\n"

    def __get_search_parameters_spoken_languages(self) -> str:
        title = f"*{phrases.search_parameters_items[constants.SearchParametersItemsIds.SPOKEN_LANGUAGES]}:* "
        raw_value = User.__DATABASE.get_users_search_parameters_spoken_languages(self.__id)
        values = User.__get_str_from_list(raw_value, mode=1)
        return title + values + "\n"

    def __get_search_parameters_programming_languages(self) -> str:
        title = f"*{phrases.search_parameters_items[constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES]}:* "
        raw_value = User.__DATABASE.get_users_search_parameters_programming_languages(self.__id)
        values = User.__get_str_from_list(raw_value, mode=1)
        return title + values + "\n"

    def __get_search_parameters_interests(self) -> str:
        title = f"*{phrases.search_parameters_items[constants.SearchParametersItemsIds.INTERESTS]}:* "
        raw_value = User.__DATABASE.get_users_search_parameters_interests(self.__id)
        values = User.__get_str_from_list(raw_value, mode=1)
        return title + values + "\n"

    # GET SEARCH PARAMETERS

    # GET USERS BY PARAMETERS

    def __get_users_by_parameters(self,
                                  age_intervals: Optional[List[List[int]]],
                                  spoken_languages: Optional[List[constants.SpokenLanguages]],
                                  programming_languages: Optional[List[constants.ProgrammingLanguages]],
                                  interests: Optional[List[constants.Interests]]):
        """
        :return: list with ids of profiles, which meet the specified criteria
        """
        all_users_ids = set(User.__DATABASE.get_all_users())
        users_ids = all_users_ids - {self.__id}  # All users ids except user's profile

        result_users_list = []

        for u_id in users_ids:  # Check all profiles
            u_age = User.__DATABASE.get_users_profile_age(u_id)
            u_spoken_languages = User.__DATABASE.get_users_profile_spoken_languages(u_id)
            u_programming_languages = User.__DATABASE.get_users_profile_programming_languages(u_id)
            u_interests = User.__DATABASE.get_users_profile_interests(u_id)

            check_age = User.__is_age_in_intervals(u_age, age_intervals)
            check_spoken_languages = User.__check_multiply_choice(spoken_languages, u_spoken_languages)
            check_programming_languages = User.__check_multiply_choice(programming_languages, u_programming_languages)
            check_interests = User.__check_multiply_choice(interests, u_interests)

            if check_age and check_spoken_languages and check_programming_languages and check_interests:
                result_users_list.append(u_id)  # Add, if profile meet the specified criteria
        return result_users_list

    @staticmethod
    def __is_age_in_intervals(age: int, age_intervals: Optional[List[List[int]]]):
        """
        :return: is the age included in at least one of the specified intervals
        """
        if age_intervals is None:
            return True
        if age is None:
            return True
        for interval in age_intervals:
            if interval[0] <= age <= interval[1]:
                return True
        return False

    @staticmethod
    def __check_multiply_choice(criteria: Optional[List[constants.Items]],
                                candidate: Optional[List[constants.Items]]) -> bool:
        """
        :return: is at least one of the candidate's parameters included in the list of criteria
        """
        if criteria is None:
            return True
        elif candidate is not None:
            return bool(len(set(criteria) & set(candidate)))
        return False

    def create_candidates_list(self) -> None:
        spoken_languages = User.__DATABASE.get_users_search_parameters_spoken_languages(self.__id)
        programming_languages = User.__DATABASE.get_users_search_parameters_programming_languages(self.__id)
        interests = User.__DATABASE.get_users_search_parameters_interests(self.__id)
        age_groups = User.__DATABASE.get_users_search_parameters_age_groups(self.__id)
        age_intervals = User.__get_age_intervals_by_age_groups(age_groups)

        candidates_ids = self.__get_users_by_parameters(age_intervals, spoken_languages, programming_languages,
                                                        interests)
        for candidate_id in candidates_ids:
            if not User.__DATABASE.is_profile_in_candidates_list(self.__id, candidate_id):
                User.__DATABASE.add_candidate(self.__id, candidate_id)

    @staticmethod
    def __get_age_intervals_by_age_groups(age_groups: Optional[List[constants.AgeGroups]]):
        """
        :return: list of intervals in format: [from: int , to: int] from list of age_groups
        """
        if age_groups is None:
            return None
        result = []
        for a_g in age_groups:
            if a_g == constants.AgeGroups.YOUNGER_THAN_14:
                result.append((0, 14))
            elif a_g == constants.AgeGroups.FROM_14_TO_18:
                result.append((14, 18))
            elif a_g == constants.AgeGroups.FROM_18_TO_25:
                result.append((18, 25))
            elif a_g == constants.AgeGroups.OLDER_THAN_25:
                result.append((25, 100))
            else:
                constants.logger.error(f"Can't create interval for age_group={a_g}")
        return result

    def get_candidate_id(self) -> Optional[int]:
        """
        :return: id of next candidate profile
        """
        candidates = User.__DATABASE.get_not_viewed_candidates(self.__id)
        if not candidates:
            return None
        return candidates[0]
