import constants


class Database:

    def __init__(self):
        self.__is_registered = True
        self.__menu_id = 1
        self.__are_search_parameters_filled = False
        self.__registration_item_id = 0
        self.__search_parameters_item_id = 0
        self.__profile = dict()
        self.__fill_profile()

    @property
    def profile(self):
        return self.__profile

    def __fill_profile(self):
        self.__profile[constants.ProfileItemsIds.FIRST_NAME.value] = "None"
        self.__profile[constants.ProfileItemsIds.LAST_NAME.value] = "None"
        self.__profile[constants.ProfileItemsIds.AGE.value] = "None"
        self.__profile[constants.ProfileItemsIds.SPOKEN_LANGUAGES.value] = ""
        self.__profile[constants.ProfileItemsIds.PROGRAMMING_LANGUAGES.value] = ""
        self.__profile[constants.ProfileItemsIds.INTERESTS.value] = ""

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

    def set_users_search_parameters_item_id(self, user_id: int,
                                            search_parameters_item_id: constants.SearchParametersItemsIds):
        self.__search_parameters_item_id = search_parameters_item_id
