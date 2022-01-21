import constants


class Database:

    def __init__(self):
        self.__is_registered = False
        self.__menu_id = 1
        self.__registration_item_id = 0
        self.__data = dict()
        self.__fill_data()

    @property
    def data(self):
        return self.__data

    def __fill_data(self):
        self.__data[constants.ProfileItemsIds.FIRST_NAME.value] = "None"
        self.__data[constants.ProfileItemsIds.LAST_NAME.value] = "None"
        self.__data[constants.ProfileItemsIds.AGE.value] = "None"
        self.__data[constants.ProfileItemsIds.SPOKEN_LANGUAGES.value] = ""
        self.__data[constants.ProfileItemsIds.PROGRAMMING_LANGUAGES.value] = ""
        self.__data[constants.ProfileItemsIds.INTERESTS.value] = ""

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

    def set_users_registration_item(self, user_id: int, item: constants.ProfileItemsIds, value: str):
        self.__data[item] = value

    def get_users_profile_item(self, user_id: int, item: int):
        return self.__data[item]

    def append_to_users_registration_item(self, user_id: int, item: constants.ProfileItemsIds, value: str):
        if item in self.__data:
            self.__data[item] = self.__data[item] + value + " "
        else:
            self.__data[item] = value

    def set_null_users_registration_item(self, user_id: int, item: constants.ProfileItemsIds):
        self.__data[item] = "None"
