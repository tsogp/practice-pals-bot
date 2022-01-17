class Database:

    def get_users_menu_id(self, telegram_id: int):
        return 1

    def get_users_registration_point_id(self, telegram_id: int):
        return 0

    def is_registrated(self, telegram_id: int):
        return False

    def write_users_registration_item(self, telegram_id: int, item: int, value: str):
        pass

    def write_empty_users_registration_item(self, telegram_id: int, item: int):
        pass

    def switch_user_to_next_registration_item(self, telegram_id: int):
        pass

    def __init__(self):
        pass
