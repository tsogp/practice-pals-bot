import database
import constants


class User:
    def __init__(self, database: database.Database, user_id: int):
        self.__database = database
        self.__id = user_id
        self.__menu_id = self.__database.get_users_menu_id(self.__id)
        self.__registration_item_id = self.__database.get_users_registration_item_id(self.__id)
        self.__search_parameter_item_id = self.__database.get_users_search_parameter_item_id(self.__id)

    def is_in_main_menu(self):
        return self.__menu_id == constants.MenuIds.MAIN_MENU

    def is_in_null_menu(self):
        return self.__menu_id == constants.MenuIds.NULL

    def is_in_check_profile_items_menu(self):
        return self.__menu_id == constants.MenuIds.CHECK_PROFILE_MENU

    def is_in_check_search_parameters_items_menu(self):
        return self.__menu_id == constants.MenuIds.CHECK_SEARCH_PARAMETERS_MENU

    def is_in_search_menu(self):
        return self.__menu_id == constants.MenuIds.SEARCH_MENU

    def is_in_registration_menu(self):
        check_menu_id = self.__menu_id == constants.MenuIds.REGISTRATION_MENU
        check_registration_item_id = self.__registration_item_id == constants.ProfileItemsIds.NULL
        return check_menu_id and check_registration_item_id

    def is_in_registration_item_first_name(self):
        check_menu_id = self.__menu_id == constants.MenuIds.REGISTRATION_MENU
        check_registration_item_id = self.__registration_item_id == constants.ProfileItemsIds.FIRST_NAME
        return check_menu_id and check_registration_item_id

    def is_in_registration_item_last_name(self):
        check_menu_id = self.__menu_id == constants.MenuIds.REGISTRATION_MENU
        check_registration_item_id = self.__registration_item_id == constants.ProfileItemsIds.LAST_NAME
        return check_menu_id and check_registration_item_id

    def is_in_registration_item_age(self):
        check_menu_id = self.__menu_id == constants.MenuIds.REGISTRATION_MENU
        check_registration_item_id = self.__registration_item_id == constants.ProfileItemsIds.AGE
        return check_menu_id and check_registration_item_id

    def is_in_registration_item_spoken_languages(self):
        check_menu_id = self.__menu_id == constants.MenuIds.REGISTRATION_MENU
        check_registration_item_id = self.__registration_item_id == constants.ProfileItemsIds.SPOKEN_LANGUAGES
        return check_menu_id and check_registration_item_id

    def is_in_registration_item_programming_languages(self):
        check_menu_id = self.__menu_id == constants.MenuIds.REGISTRATION_MENU
        check_registration_item_id = self.__registration_item_id == constants.ProfileItemsIds.PROGRAMMING_LANGUAGES
        return check_menu_id and check_registration_item_id

    def is_in_registration_item_interests(self):
        check_menu_id = self.__menu_id == constants.MenuIds.REGISTRATION_MENU
        check_registration_item_id = self.__registration_item_id == constants.ProfileItemsIds.INTERESTS
        return check_menu_id and check_registration_item_id

    def is_in_search_parameter_item_age_group(self):
        check_menu_id = self.__menu_id == constants.MenuIds.SEARCH_PARAMETERS_MENU
        check_search_parameter_item_id = self.__search_parameter_item_id == constants.SearchParametersItemsIds.AGE_GROUP
        return check_menu_id and check_search_parameter_item_id

    def is_in_search_parameter_item_spoken_languages(self):
        check_menu_id = self.__menu_id == constants.MenuIds.SEARCH_PARAMETERS_MENU
        check_search_parameter_item_id = self.__search_parameter_item_id == constants.SearchParametersItemsIds.SPOKEN_LANGUAGES
        return check_menu_id and check_search_parameter_item_id

    def is_in_search_parameter_item_programming_languages(self):
        check_menu_id = self.__menu_id == constants.MenuIds.SEARCH_PARAMETERS_MENU
        check_search_parameter_item_id = self.__search_parameter_item_id == constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES
        return check_menu_id and check_search_parameter_item_id

    def is_in_search_parameter_item_interests(self):
        check_menu_id = self.__menu_id == constants.MenuIds.SEARCH_PARAMETERS_MENU
        check_search_parameter_item_id = self.__search_parameter_item_id == constants.SearchParametersItemsIds.INTERESTS
        return check_menu_id and check_search_parameter_item_id
