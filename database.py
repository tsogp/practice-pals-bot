class Database:

    def get_users_menu_id(self, telegram_id: int):
        return self.__menu_id

    def get_users_registration_item_id(self, telegram_id: int):
        return self.__registration_item_id

    def is_registrated(self, telegram_id: int):
        return self.__is_registrated

    def write_users_registration_item(self, telegram_id: int, item: int, value: str):
        pass

    def write_empty_users_registration_item(self, telegram_id: int, item: int):
        pass

    def switch_user_to_next_registration_item(self, telegram_id: int):
        self.__registration_item_id += 1

    def __init__(self):
        self.__is_registrated = False
        self.__menu_id = 1
        self.__registration_item_id = 0
