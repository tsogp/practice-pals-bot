from IDatabase import IDatabase
import constants
import phrases_ru as phrases


class User:
    __DATABASE = None  # Bot's database object

    @classmethod
    def set_database(cls, database: IDatabase) -> None:
        """
        Set bot's database object.
        MUST BE CALLED BEFORE CREATING OBJECTS!
        """
        cls.__DATABASE = database

    def __init__(self, user_id: int):
        self.__id = user_id
        self.__menu_id = User.__DATABASE.get_users_menu_id(self.__id)
        self.__registration_item_id = User.__DATABASE.get_users_registration_item_id(self.__id)
        self.__search_parameter_item_id = User.__DATABASE.get_users_search_parameter_item_id(self.__id)

    def is_in_menu(self, menu_id: constants.MenuIds) -> bool:
        """
        Check, is user in menu with menu_id
        """
        return self.__menu_id == menu_id

    def is_in_registration_item(self, profile_item_id: constants.ProfileItemsIds) -> bool:
        """
        Check, is user filling registration_item with profile_item_id
        """
        check_menu_id = self.__menu_id == constants.MenuIds.REGISTRATION_MENU
        check_registration_item_id = self.__registration_item_id == profile_item_id
        return check_menu_id and check_registration_item_id

    def is_in_search_parameters_item(self, search_parameters_item_id: constants.SearchParametersItemsIds) -> bool:
        """
        Check, is user filling search parameter with search_parameters_item_id
        """
        check_menu_id = self.__menu_id == constants.MenuIds.SEARCH_PARAMETERS_MENU
        check_search_parameter_item_id = self.__search_parameter_item_id == search_parameters_item_id
        return check_menu_id and check_search_parameter_item_id

    def is_like_acceptable(self) -> bool:
        return User.__DATABASE.get_number_of_likes(self.__id) < constants.MAXIMUM_NUMBER_OF_LIKES

    def get_profile(self) -> str:
        """
        :return: list of profile items and it's values in string with markdown
        """
        profile = ""
        profile_items_ids = [member for member in constants.ProfileItemsIds if member.name != "NULL"]
        for profile_item_id in profile_items_ids:
            raw_value = User.__DATABASE.get_users_profile_item(self.__id, profile_item_id)
            profile += (f"*{phrases.profile_items[profile_item_id]}:* " +
                        (raw_value if raw_value is not None else (
                                "_" + phrases.item_is_not_specified + "_")) + "\n")
        return profile

    def get_search_parameters(self) -> str:
        """
        :return: list of search parameters items and it's values in string with markdown
        """
        search_parameters = ""
        search_parameters_items_ids = [member for member in constants.SearchParametersItemsIds if
                                       member.name != "NULL"]
        for search_parameters_item_id in search_parameters_items_ids:
            raw_value = User.__DATABASE.get_users_search_parameter_item(self.__id, search_parameters_item_id)
            search_parameters += (f"*{phrases.search_parameters_items[search_parameters_item_id]}:* " +
                                  (raw_value if raw_value is not None else (
                                          "_" + phrases.item_is_not_specified + "_")) + "\n")
        return search_parameters
