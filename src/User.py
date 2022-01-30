import database
import constants


class User:
    def __init__(self, database: database.Database, user_id: int):
        self.__database = database
        self.__id = user_id
        self.__menu_id = self.__database.get_users_menu_id(self.__id)
        self.__registration_item_id = self.__database.get_users_registration_item_id(self.__id)
        self.__search_parameter_item_id = self.__database.get_users_search_parameter_item_id(self.__id)

    def is_in_menu(self, menu_id: constants.MenuIds):
        return self.__menu_id == menu_id

    def is_in_registration_item(self, profile_item_id: constants.ProfileItemsIds):
        check_menu_id = self.__menu_id == constants.MenuIds.REGISTRATION_MENU
        check_registration_item_id = self.__registration_item_id == profile_item_id
        return check_menu_id and check_registration_item_id

    def is_in_search_parameters_item(self, search_parameters_item_id: constants.SearchParametersItemsIds):
        check_menu_id = self.__menu_id == constants.MenuIds.SEARCH_PARAMETERS_MENU
        check_search_parameter_item_id = self.__search_parameter_item_id == search_parameters_item_id
        return check_menu_id and check_search_parameter_item_id
