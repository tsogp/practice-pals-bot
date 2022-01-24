import telebot
import phrases_ru as phrases
import constants
from keyboards import Keyboards

import bottoken
from database import Database


class Bot:
    __bot = telebot.TeleBot(bottoken.TOKEN)  # Main bot object
    __database = Database()

    @staticmethod
    def run():
        Bot.__bot.polling(none_stop=True)

    @__bot.message_handler(commands=['start'])
    @staticmethod
    def __start(message):
        """
        Processing the command "/start"
        """
        Bot.__bot.send_message(message.chat.id,
                               text=phrases.welcome_message,
                               reply_markup=telebot.types.ReplyKeyboardRemove())
        Bot.__check_registration(message.chat.id)

    @__bot.message_handler(commands=['main_menu'])
    @staticmethod
    def __main_menu(message):
        """
        Processing the command "/main_menu"
        """
        Bot.__activate_main_menu(message.chat.id)

    @__bot.message_handler(content_types=["text"])
    @staticmethod
    def __processing_all_text_messages(message):
        users_message = message.text
        users_menu_id = Bot.__database.get_users_menu_id(message.chat.id)
        if users_menu_id == constants.MenuIds.REGISTRATION_MENU:
            Bot.__processing_registration_menu_items(users_message, message.chat.id)
        elif users_menu_id == constants.MenuIds.CHECK_PROFILE_MENU:
            Bot.__processing_check_profile_items_menu(users_message, message.chat.id)
        elif users_menu_id == constants.MenuIds.MAIN_MENU:
            Bot.__processing_main_menu_items(users_message, message.chat.id)
        elif users_menu_id == constants.MenuIds.SEARCH_PARAMETERS_MENU:
            Bot.__processing_search_parameters_menu_items(users_message, message.chat.id)
        elif users_menu_id == constants.MenuIds.CHECK_SEARCH_PARAMETERS_MENU:
            Bot.__processing_check_search_parameters_items_menu(users_message, message.chat.id)
        elif users_menu_id == constants.MenuIds.SEARCH_MENU:
            Bot.__processing_search_menu_items(users_message, message.chat.id)
        else:
            Bot.__bot.send_message(message.chat.id, text=phrases.call_main_menu)

    @staticmethod
    def __check_registration(user_id: int):
        if Bot.__database.is_registered(user_id):
            Bot.__activate_main_menu(user_id)
        else:  # Start registration procedure
            Bot.__bot.send_message(user_id, text=phrases.user_not_registered_yet)
            Bot.__bot.send_message(user_id, text=phrases.enter_your_first_name,
                                   reply_markup=Keyboards.profile_do_not_specify)
            Bot.__database.set_users_menu_id(user_id, constants.MenuIds.REGISTRATION_MENU)
            Bot.__database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.FIRST_NAME)

    @staticmethod
    def __check_search_parameters(user_id: int):
        if Bot.__database.are_search_parameters_filled(user_id):
            Bot.__activate_search_menu(user_id)
        else:  # Start filling search parameters procedure
            Bot.__bot.send_message(user_id, text=phrases.user_have_not_search_parameters_yet)
            Bot.__bot.send_message(user_id, text=phrases.enter_age_group_for_search,
                                   reply_markup=Keyboards.search_parameters_age_groups)
            Bot.__database.set_users_menu_id(user_id, constants.MenuIds.SEARCH_PARAMETERS_MENU)
            Bot.__database.set_users_search_parameter_item_id(user_id, constants.SearchParametersItemsIds.AGE_GROUP)

    @staticmethod
    def __activate_main_menu(user_id: int):
        Bot.__database.set_users_menu_id(user_id, constants.MenuIds.MAIN_MENU)
        Bot.__bot.send_message(user_id, text=phrases.main_menu_title,
                               reply_markup=Keyboards.main_menu)

    @staticmethod
    def __activate_search_menu(user_id: int):
        Bot.__database.set_users_menu_id(user_id, constants.MenuIds.SEARCH_MENU)
        Bot.__bot.send_message(user_id, text=phrases.search_menu_title,
                               reply_markup=Keyboards.search_menu)

    @staticmethod
    def __show_users_profile(user_id: int):
        """
        Send a message to the user with his profile
        """
        Bot.__database.set_users_menu_id(user_id, constants.MenuIds.CHECK_PROFILE_MENU)
        Bot.__bot.send_message(user_id, text=phrases.your_profile)
        Bot.__bot.send_message(user_id, text=Bot.__generate_string_with_users_profile(user_id),
                               parse_mode="Markdown",
                               reply_markup=Keyboards.profile_ok_edit)

    @staticmethod
    def __generate_string_with_users_profile(user_id: int):
        profile_str = ""
        profile_items_ids = [member for member in constants.ProfileItemsIds if member.name != "NULL"]
        for profile_item_id in profile_items_ids:
            profile_str += (f"*{phrases.profile_items[profile_item_id]}:* " +
                            Bot.__database.get_users_profile_item(user_id, profile_item_id) + "\n")
        return profile_str

    @staticmethod
    def __show_users_search_parameters(user_id: int):
        """
        Send a message to the user with his search_parameters
        """
        Bot.__database.set_users_menu_id(user_id, constants.MenuIds.CHECK_SEARCH_PARAMETERS_MENU)
        Bot.__bot.send_message(user_id, text=phrases.your_search_parameters)
        Bot.__bot.send_message(user_id, text=Bot.__generate_string_with_users_search_parameters(user_id),
                               parse_mode="Markdown",
                               reply_markup=Keyboards.search_parameters_ok_edit)

    @staticmethod
    def __generate_string_with_users_search_parameters(user_id: int):
        search_parameters_str = ""
        search_parameters_items_ids = [member for member in constants.SearchParametersItemsIds if
                                       member.name != "NULL"]
        for search_parameters_item_id in search_parameters_items_ids:
            search_parameters_str += (f"*{phrases.search_parameters_items[search_parameters_item_id]}:* " +
                                      Bot.__database.get_users_search_parameter_item(user_id,
                                                                                     search_parameters_item_id) + "\n")
        return search_parameters_str

    @staticmethod
    def __processing_main_menu_items(users_message: str, user_id: int):
        if users_message == phrases.main_menu_list[0]:
            Bot.__check_search_parameters(user_id)
        elif users_message == phrases.main_menu_list[1]:
            Bot.__bot.send_message(user_id, text=phrases.not_ready_yet)
        elif users_message == phrases.main_menu_list[2]:
            Bot.__bot.send_message(user_id, text=phrases.not_ready_yet)

    @staticmethod
    def __processing_check_profile_items_menu(users_message: str, user_id: int):
        if users_message == phrases.ok_edit[0]:
            Bot.__activate_main_menu(user_id)
        elif users_message == phrases.ok_edit[1]:
            Bot.__bot.send_message(user_id, text=phrases.not_ready_yet)
            Bot.__activate_main_menu(user_id)

    @staticmethod
    def __processing_check_search_parameters_items_menu(users_message: str, user_id: int):
        if users_message == phrases.ok_edit[0]:
            Bot.__activate_search_menu(user_id)
        elif users_message == phrases.ok_edit[1]:
            Bot.__bot.send_message(user_id, text=phrases.not_ready_yet)
            Bot.__activate_search_menu(user_id)

    @staticmethod
    def __processing_registration_menu_items(users_message: str, user_id: int):
        users_registration_item_id = Bot.__database.get_users_registration_item_id(user_id)
        if users_registration_item_id == constants.ProfileItemsIds.FIRST_NAME:
            Bot.__processing_registration_item_first_name(users_message, user_id)
        elif users_registration_item_id == constants.ProfileItemsIds.LAST_NAME:
            Bot.__processing_registration_item_last_name(users_message, user_id)
        elif users_registration_item_id == constants.ProfileItemsIds.AGE:
            Bot.__processing_registration_item_age(users_message, user_id)
        elif users_registration_item_id == constants.ProfileItemsIds.SPOKEN_LANGUAGES:
            Bot.__processing_registration_item_spoken_language(users_message, user_id)
        elif users_registration_item_id == constants.ProfileItemsIds.PROGRAMMING_LANGUAGES:
            Bot.__processing_registration_item_programming_language(users_message, user_id)
        elif users_registration_item_id == constants.ProfileItemsIds.INTERESTS:
            Bot.__processing_registration_item_interests(users_message, user_id)

    @staticmethod
    def __processing_registration_item_first_name(users_message: str, user_id: int):
        if users_message == phrases.do_not_specify:
            Bot.__database.set_null_users_registration_item(user_id,
                                                            item=constants.ProfileItemsIds.FIRST_NAME)
        else:
            Bot.__database.set_users_registration_item(user_id,
                                                       item=constants.ProfileItemsIds.FIRST_NAME,
                                                       value=users_message)

        Bot.__database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.LAST_NAME)
        Bot.__bot.send_message(user_id, text=phrases.enter_your_last_name)

    @staticmethod
    def __processing_registration_item_last_name(users_message: str, user_id: int):
        if users_message == phrases.do_not_specify:
            Bot.__database.set_null_users_registration_item(user_id,
                                                            item=constants.ProfileItemsIds.LAST_NAME)
        else:
            Bot.__database.set_users_registration_item(user_id,
                                                       item=constants.ProfileItemsIds.LAST_NAME,
                                                       value=users_message)

        Bot.__database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.AGE)
        Bot.__bot.send_message(user_id, text=phrases.enter_your_age)

    @staticmethod
    def __processing_registration_item_age(users_message: str, user_id: int):
        if users_message == phrases.do_not_specify:
            Bot.__database.set_null_users_registration_item(user_id, item=constants.ProfileItemsIds.AGE)
        elif users_message.isdigit():
            Bot.__database.set_users_registration_item(user_id,
                                                       item=constants.ProfileItemsIds.AGE,
                                                       value=users_message)
        else:
            Bot.__bot.send_message(user_id, text=phrases.enter_correct_age)

        if users_message == phrases.do_not_specify or users_message.isdigit():
            Bot.__database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.SPOKEN_LANGUAGES)
            Bot.__bot.send_message(user_id, text=phrases.enter_your_spoken_languages,
                                   reply_markup=Keyboards.profile_spoken_languages)

    @staticmethod
    def __processing_registration_item_spoken_language(users_message: str, user_id: int):
        if users_message == phrases.do_not_specify:
            Bot.__database.set_null_users_registration_item(user_id,
                                                            item=constants.ProfileItemsIds.SPOKEN_LANGUAGES)
        elif users_message in phrases.spoken_languages:
            Bot.__database.append_to_users_registration_item(user_id,
                                                             item=constants.ProfileItemsIds.SPOKEN_LANGUAGES,
                                                             value=users_message)
        elif users_message != phrases.finish_typing:
            Bot.__bot.send_message(user_id, text=phrases.select_from_the_list)

        if users_message in (phrases.do_not_specify, phrases.finish_typing):
            Bot.__database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.PROGRAMMING_LANGUAGES)
            Bot.__bot.send_message(user_id, text=phrases.enter_your_programming_languages,
                                   reply_markup=Keyboards.profile_programming_languages)

    @staticmethod
    def __processing_registration_item_programming_language(users_message: str, user_id: int):
        if users_message == phrases.do_not_specify:
            Bot.__database.set_null_users_registration_item(user_id,
                                                            item=constants.ProfileItemsIds.PROGRAMMING_LANGUAGES)
        elif users_message in phrases.programming_languages:
            Bot.__database.append_to_users_registration_item(user_id,
                                                             item=constants.ProfileItemsIds.PROGRAMMING_LANGUAGES,
                                                             value=users_message)
        elif users_message != phrases.finish_typing:
            Bot.__bot.send_message(user_id, text=phrases.select_from_the_list)

        if users_message in (phrases.do_not_specify, phrases.finish_typing):
            Bot.__database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.INTERESTS)
            Bot.__bot.send_message(user_id, text=phrases.enter_your_interests,
                                   reply_markup=Keyboards.profile_interests)

    @staticmethod
    def __processing_registration_item_interests(users_message: str, user_id: int):
        if users_message == phrases.do_not_specify:
            Bot.__database.set_null_users_registration_item(user_id,
                                                            item=constants.ProfileItemsIds.INTERESTS)
        elif users_message in phrases.interests:
            Bot.__database.append_to_users_registration_item(user_id,
                                                             item=constants.ProfileItemsIds.INTERESTS,
                                                             value=users_message)
        elif users_message != phrases.finish_typing:
            Bot.__bot.send_message(user_id, text=phrases.select_from_the_list)

        if users_message in (phrases.do_not_specify, phrases.finish_typing):
            Bot.__database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.NULL)
            Bot.__bot.send_message(user_id, text=phrases.finish_registration,
                                   reply_markup=telebot.types.ReplyKeyboardRemove())
            Bot.__show_users_profile(user_id)

    @staticmethod
    def __processing_search_parameters_menu_items(users_message: str, user_id: int):
        users_search_parameter_item_id = Bot.__database.get_users_search_parameter_item_id(user_id)
        if users_search_parameter_item_id == constants.SearchParametersItemsIds.AGE_GROUP:
            Bot.__processing_search_parameter_item_age_group(users_message, user_id)
        elif users_search_parameter_item_id == constants.SearchParametersItemsIds.SPOKEN_LANGUAGES:
            Bot.__processing_search_parameter_item_spoken_languages(users_message, user_id)
        elif users_search_parameter_item_id == constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES:
            Bot.__processing_search_parameter_item_programming_languages(users_message, user_id)
        elif users_search_parameter_item_id == constants.SearchParametersItemsIds.INTERESTS:
            Bot.__processing_search_parameter_item_interests(users_message, user_id)

    @staticmethod
    def __processing_search_parameter_item_age_group(users_message: str, user_id: int):
        if users_message == phrases.does_not_matter:
            Bot.__database.set_null_users_search_parameter_item(user_id,
                                                                item=constants.SearchParametersItemsIds.AGE_GROUP)
        elif users_message in phrases.age_groups:
            Bot.__database.append_to_users_search_parameter_item(user_id,
                                                                 item=constants.SearchParametersItemsIds.AGE_GROUP,
                                                                 value=users_message)
        elif users_message != phrases.finish_typing:
            Bot.__bot.send_message(user_id, text=phrases.select_from_the_list)

        if users_message in (phrases.does_not_matter, phrases.finish_typing):
            Bot.__database.set_users_search_parameter_item_id(user_id,
                                                              constants.SearchParametersItemsIds.SPOKEN_LANGUAGES)
            Bot.__bot.send_message(user_id, text=phrases.enter_spoken_languages,
                                   reply_markup=Keyboards.search_parameters_spoken_languages)

    @staticmethod
    def __processing_search_parameter_item_spoken_languages(users_message: str, user_id: int):
        if users_message == phrases.does_not_matter:
            Bot.__database.set_null_users_search_parameter_item(user_id,
                                                                item=constants.SearchParametersItemsIds.SPOKEN_LANGUAGES)
        elif users_message in phrases.spoken_languages:
            Bot.__database.append_to_users_search_parameter_item(user_id,
                                                                 item=constants.SearchParametersItemsIds.SPOKEN_LANGUAGES,
                                                                 value=users_message)
        elif users_message != phrases.finish_typing:
            Bot.__bot.send_message(user_id, text=phrases.select_from_the_list)

        if users_message in (phrases.does_not_matter, phrases.finish_typing):
            Bot.__database.set_users_search_parameter_item_id(user_id,
                                                              constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES)
            Bot.__bot.send_message(user_id, text=phrases.enter_programming_languages,
                                   reply_markup=Keyboards.search_parameters_programming_languages)

    @staticmethod
    def __processing_search_parameter_item_programming_languages(users_message: str, user_id: int):
        if users_message == phrases.does_not_matter:
            Bot.__database.set_null_users_search_parameter_item(user_id,
                                                                item=constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES)
        elif users_message in phrases.programming_languages:
            Bot.__database.append_to_users_search_parameter_item(user_id,
                                                                 item=constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES,
                                                                 value=users_message)
        elif users_message != phrases.finish_typing:
            Bot.__bot.send_message(user_id, text=phrases.select_from_the_list)

        if users_message in (phrases.does_not_matter, phrases.finish_typing):
            Bot.__database.set_users_search_parameter_item_id(user_id,
                                                              constants.SearchParametersItemsIds.INTERESTS)
            Bot.__bot.send_message(user_id, text=phrases.enter_interests,
                                   reply_markup=Keyboards.search_parameters_interests)

    @staticmethod
    def __processing_search_parameter_item_interests(users_message: str, user_id: int):
        if users_message == phrases.does_not_matter:
            Bot.__database.set_null_users_search_parameter_item(user_id,
                                                                item=constants.SearchParametersItemsIds.INTERESTS)
        elif users_message in phrases.interests:
            Bot.__database.append_to_users_search_parameter_item(user_id,
                                                                 item=constants.SearchParametersItemsIds.INTERESTS,
                                                                 value=users_message)
        elif users_message != phrases.finish_typing:
            Bot.__bot.send_message(user_id, text=phrases.select_from_the_list)

        if users_message in (phrases.does_not_matter, phrases.finish_typing):
            Bot.__database.set_users_search_parameter_item_id(user_id,
                                                              constants.SearchParametersItemsIds.NULL)
            Bot.__bot.send_message(user_id, text=phrases.finish_enter_search_parameters,
                                   reply_markup=telebot.types.ReplyKeyboardRemove())
            Bot.__show_users_search_parameters(user_id)

    @staticmethod
    def __processing_search_menu_items(users_message: str, user_id: int):
        if users_message == phrases.search_menu_list[0]:
            Bot.__bot.send_message(user_id, text=phrases.not_ready_yet)
        elif users_message == phrases.search_menu_list[1]:
            Bot.__bot.send_message(user_id, text=phrases.not_ready_yet)
        elif users_message == phrases.search_menu_list[2]:
            Bot.__bot.send_message(user_id, text=phrases.not_ready_yet)
