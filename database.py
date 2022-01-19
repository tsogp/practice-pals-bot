class Database:

    def __init__(self):
        self.__is_registrated = False
        self.__menu_id = 1
        self.__registration_item_id = 0
        self.__data = dict()
        self.__fill_data()

    @property
    def data(self):
        return self.__data

    def __fill_data(self):
        self.__data[0] = "None"
        self.__data[1] = "None"
        self.__data[2] = "None"
        self.__data[3] = ""
        self.__data[4] = ""
        self.__data[5] = ""

    def set_users_menu_id(self, telegram_id: int, new_menu_id: int):
        self.__menu_id = new_menu_id

    def get_users_menu_id(self, telegram_id: int):
        return self.__menu_id

    def get_users_registration_item_id(self, telegram_id: int):
        return self.__registration_item_id

    def is_registrated(self, telegram_id: int):
        return self.__is_registrated

    def set_users_registration_item(self, telegram_id: int, item: int, value: str):
        self.__data[item] = value

    def get_users_profile_item(self, telegram_id: int, item: int):
        return self.__data[item]

    def append_to_users_registration_item(self, telegram_id: int, item: int, value: str):
        if item in self.__data:
            self.__data[item] = self.__data[item] + " " + value
        else:
            self.__data[item] = value

    def set_null_users_registration_item(self, telegram_id: int, item: int):
        self.__data[item] = "None"

    def switch_user_to_next_registration_item(self, telegram_id: int):
        self.__registration_item_id += 1
