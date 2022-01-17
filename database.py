class Database:

    def __init__(self):
        self.__is_registrated = False
        self.__menu_id = 1
        self.__registration_item_id = 0
        self.__data = dict()

    @property
    def data(self):
        return self.__data

    def get_users_menu_id(self, telegram_id: int):
        return self.__menu_id

    def get_users_registration_item_id(self, telegram_id: int):
        return self.__registration_item_id

    def is_registrated(self, telegram_id: int):
        return self.__is_registrated

    def set_users_registration_item(self, telegram_id: int, item: int, value: str):
        self.__data[item] = value

    def append_to_users_registration_item(self, telegram_id: int, item: int, value: str):
        if item in self.__data:
            self.__data[item] = self.__data[item] + " " + value
        else:
            self.__data[item] = value

    def set_null_users_registration_item(self, telegram_id: int, item: int):
        self.__data[item] = None

    def switch_user_to_next_registration_item(self, telegram_id: int):
        self.__registration_item_id += 1
