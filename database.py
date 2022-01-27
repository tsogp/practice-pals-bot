# File with fake database class
import constants


class Database:

    def __init__(self):
        self.__is_registered = False
        self.__menu_id = constants.MenuIds.MAIN_MENU
        self.__are_search_parameters_filled = True
        self.__registration_item_id = constants.ProfileItemsIds.NULL
        self.__search_parameter_item_id = constants.SearchParametersItemsIds.NULL
        self.__profile = dict()
        self.__fill_profile()
        self.__search_parameters = dict()
        self.__fill_search_parameters()

        self.__shown_profile_id = None

        self.__telegram_id = None
        self.__telegram_login = "@yu_leo"

        self.__remaining_number_of_likes = constants.MAXIMUM_NUMBER_OF_LIKES

    @property
    def profile(self):
        return self.__profile

    @property
    def search_parameters(self):
        return self.__search_parameters

    def __fill_profile(self):
        self.__profile[constants.ProfileItemsIds.FIRST_NAME] = "None"
        self.__profile[constants.ProfileItemsIds.LAST_NAME] = "None"
        self.__profile[constants.ProfileItemsIds.AGE] = "None"
        self.__profile[constants.ProfileItemsIds.SPOKEN_LANGUAGES] = ""
        self.__profile[constants.ProfileItemsIds.PROGRAMMING_LANGUAGES] = ""
        self.__profile[constants.ProfileItemsIds.INTERESTS] = ""

    def __fill_search_parameters(self):
        self.__search_parameters[constants.SearchParametersItemsIds.AGE_GROUP] = ""
        self.__search_parameters[constants.SearchParametersItemsIds.SPOKEN_LANGUAGES] = ""
        self.__search_parameters[constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES] = ""
        self.__search_parameters[constants.SearchParametersItemsIds.INTERESTS] = ""

    def set_users_menu_id(self, user_id: int, new_menu_id: constants.MenuIds):
        self.__menu_id = new_menu_id

    def get_users_menu_id(self, user_id: int):
        return self.__menu_id

    def get_users_registration_item_id(self, user_id: int):
        return self.__registration_item_id

    def set_users_registration_item_id(self, user_id: int, registration_item_id: constants.ProfileItemsIds):
        self.__registration_item_id = registration_item_id

    def is_registered(self, user_id: int):
        return self.__is_registered

    def register_user(self, user_id: int, user_name: str):
        self.__is_registered = True
        self.__telegram_id = user_id
        self.__telegram_login = "@" + user_name

    def are_search_parameters_filled(self, user_id: int):
        return self.__are_search_parameters_filled

    def set_users_registration_item(self, user_id: int, item: constants.ProfileItemsIds, value: str):
        self.__profile[item] = value

    def get_users_profile_item(self, user_id: int, item: int):
        return self.__profile[item]

    def append_to_users_registration_item(self, user_id: int, item: constants.ProfileItemsIds, value: str):
        if item in self.__profile:
            self.__profile[item] = self.__profile[item] + value + " "
        else:
            self.__profile[item] = value

    def set_null_users_registration_item(self, user_id: int, item: constants.ProfileItemsIds):
        self.__profile[item] = "None"

    def set_users_search_parameter_item_id(self, user_id: int,
                                           search_parameter_item_id: constants.SearchParametersItemsIds):
        self.__search_parameter_item_id = search_parameter_item_id

    def get_users_search_parameter_item_id(self, user_id: int):
        return self.__search_parameter_item_id

    def set_null_users_search_parameter_item(self, user_id: int, item: constants.SearchParametersItemsIds):
        self.__search_parameters[item] = "None"

    def append_to_users_search_parameter_item(self, user_id: int, item: constants.SearchParametersItemsIds, value: str):
        if item in self.__search_parameters:
            self.__search_parameters[item] = self.__search_parameters[item] + value + " "
        else:
            self.__search_parameters[item] = value

    def get_users_search_parameter_item(self, user_id: int, item: constants.SearchParametersItemsIds):
        return self.__search_parameters[item]

    def set_users_shown_profile_id(self, user_id: int, candidate_id):
        self.__shown_profile_id = candidate_id

    def get_users_shown_profile_id(self, user_id: int):
        return self.__shown_profile_id

    def get_users_telegram_login_by_id(self, user_id: int):
        return self.__telegram_login

    def dec_remaining_number_of_likes(self, user_id: int):
        self.__remaining_number_of_likes -= 1

    def get_remaining_number_of_likes(self, user_id: int):
        return self.__remaining_number_of_likes
