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
    def start(message):
        Bot.__bot.send_message(message.chat.id,
                               text=phrases.welcome_message,
                               reply_markup=telebot.types.ReplyKeyboardRemove())
        Bot.__check_registration(message.chat.id)

    @__bot.message_handler(commands=['main_menu'])
    @staticmethod
    def __main_menu(message):
        Bot.__database.set_users_menu_id(message.chat.id, constants.MenuIds.MAIN_MENU)
        Bot.__activate_main_menu(message.chat.id)

    @__bot.message_handler(content_types=["text"])
    @staticmethod
    def __processing_all_text_messages(message):
        users_message = message.text
        users_menu_id = Bot.__database.get_users_menu_id(user_id=message.chat.id)
        if users_menu_id == constants.MenuIds.REGISTRATION_MENU:
            Bot.__processing_registration_menu_items(users_message, message.chat.id)
        elif users_menu_id == constants.MenuIds.CHECK_PROFILE_MENU:
            Bot.__processing_check_profile_menu_items(users_message, message.chat.id)
        elif users_menu_id == constants.MenuIds.MAIN_MENU:
            Bot.__processing_main_menu_items(users_message, message.chat.id)
        else:
            Bot.__bot.send_message(message.chat.id, text=phrases.call_main_menu)

    @staticmethod
    def __check_registration(user_id: int):
        if Bot.__database.is_registered(user_id):
            Bot.__activate_main_menu(user_id)
        else:  # Start registration procedure
            Bot.__bot.send_message(user_id, text=phrases.user_not_registered_yet)
            Bot.__bot.send_message(user_id, text=phrases.enter_your_first_name,
                                   reply_markup=Keyboards.keyboard_do_not_specify)

    @staticmethod
    def __activate_main_menu(user_id: int):
        Bot.__database.set_users_menu_id(user_id, constants.MenuIds.MAIN_MENU)
        Bot.__bot.send_message(user_id, text=phrases.main_menu_title,
                               reply_markup=Keyboards.keyboard_main_menu)

    @staticmethod
    def __show_users_profile(user_id: int):
        """
        Send a message to the user with his profile
        """
        Bot.__bot.send_message(user_id, text=phrases.your_profile)
        Bot.__bot.send_message(user_id, text=Bot.__generate_string_with_users_profile(user_id),
                               parse_mode="Markdown",
                               reply_markup=Keyboards.keyboard_ok_edit)
        Bot.__database.set_users_menu_id(user_id, constants.MenuIds.CHECK_PROFILE_MENU)

    @staticmethod
    def __generate_string_with_users_profile(user_id: int):
        profile_str = ""
        for profile_item_id in constants.ProfileItemsIds.ITEMS_IDS:
            profile_str += (f"*{phrases.profile_items[profile_item_id]}:* " +
                            Bot.__database.get_users_profile_item(user_id, profile_item_id) + "\n")
        return profile_str

    @staticmethod
    def __processing_main_menu_items(users_message: str, user_id: int):
        if users_message == phrases.main_menu_list[0]:
            Bot.__bot.send_message(user_id, text=phrases.not_ready_yet)
        elif users_message == phrases.main_menu_list[1]:
            Bot.__bot.send_message(user_id, text=phrases.not_ready_yet)
        elif users_message == phrases.main_menu_list[2]:
            Bot.__bot.send_message(user_id, text=phrases.not_ready_yet)

    @staticmethod
    def __processing_check_profile_menu_items(users_message: str, user_id: int):
        if users_message == phrases.ok_edit[0]:
            Bot.__activate_main_menu(user_id)
        elif users_message == phrases.ok_edit[1]:
            Bot.__bot.send_message(user_id, text=phrases.not_ready_yet)
            Bot.__activate_main_menu(user_id)

    @staticmethod
    def __processing_registration_menu_items(users_message: str, user_id: int):
        users_registration_item_id = Bot.__database.get_users_registration_item_id(user_id=user_id)
        if users_registration_item_id == constants.ProfileItemsIds.FIRST_NAME:
            Bot.__processing_registration_item_first_name(users_message, user_id=user_id)
        elif users_registration_item_id == constants.ProfileItemsIds.LAST_NAME:
            Bot.__processing_registration_item_last_name(users_message, user_id=user_id)
        elif users_registration_item_id == constants.ProfileItemsIds.AGE:
            Bot.__processing_registration_item_age(users_message, user_id=user_id)
        elif users_registration_item_id == constants.ProfileItemsIds.SPOKEN_LANGUAGES:
            Bot.__processing_registration_item_spoken_language(users_message, user_id=user_id)
        elif users_registration_item_id == constants.ProfileItemsIds.PROGRAMMING_LANGUAGES:
            Bot.__processing_registration_item_programming_language(users_message, user_id=user_id)
        elif users_registration_item_id == constants.ProfileItemsIds.INTERESTS:
            Bot.__processing_registration_item_interests(users_message, user_id=user_id)

    @staticmethod
    def __processing_registration_item_first_name(users_message: str, user_id: int):
        if users_message == phrases.do_not_specify:
            Bot.__database.set_null_users_registration_item(user_id=user_id,
                                                            item=constants.ProfileItemsIds.FIRST_NAME)
        else:
            Bot.__database.set_users_registration_item(user_id=user_id,
                                                       item=constants.ProfileItemsIds.FIRST_NAME,
                                                       value=users_message)

        Bot.__database.switch_user_to_next_registration_item(user_id=user_id)
        Bot.__bot.send_message(user_id, text=phrases.enter_your_last_name)

    @staticmethod
    def __processing_registration_item_last_name(users_message: str, user_id: int):
        if users_message == phrases.do_not_specify:
            Bot.__database.set_null_users_registration_item(user_id=user_id,
                                                            item=constants.ProfileItemsIds.LAST_NAME)
        else:
            Bot.__database.set_users_registration_item(user_id=user_id,
                                                       item=constants.ProfileItemsIds.LAST_NAME,
                                                       value=users_message)

        Bot.__database.switch_user_to_next_registration_item(user_id=user_id)
        Bot.__bot.send_message(user_id, text=phrases.enter_your_age)

    @staticmethod
    def __processing_registration_item_age(users_message: str, user_id: int):
        if users_message == phrases.do_not_specify:
            Bot.__database.set_null_users_registration_item(user_id=user_id,
                                                            item=constants.ProfileItemsIds.AGE)
        else:
            Bot.__database.set_users_registration_item(user_id=user_id,
                                                       item=constants.ProfileItemsIds.AGE,
                                                       value=users_message)

        Bot.__database.switch_user_to_next_registration_item(user_id=user_id)
        Bot.__bot.send_message(user_id, text=phrases.enter_your_spoken_languages,
                               reply_markup=Keyboards.keyboard_spoken_languages)

    @staticmethod
    def __processing_registration_item_spoken_language(users_message: str, user_id: int):
        if users_message == phrases.do_not_specify:
            Bot.__database.set_null_users_registration_item(user_id=user_id,
                                                            item=constants.ProfileItemsIds.SPOKEN_LANGUAGES)
        elif users_message in phrases.spoken_languages:
            Bot.__database.append_to_users_registration_item(user_id=user_id,
                                                             item=constants.ProfileItemsIds.SPOKEN_LANGUAGES,
                                                             value=users_message)
        elif users_message != phrases.finish_typing:
            Bot.__bot.send_message(user_id, text=phrases.select_from_the_list)

        if users_message in (phrases.do_not_specify, phrases.finish_typing):
            Bot.__database.switch_user_to_next_registration_item(user_id=user_id)
            Bot.__bot.send_message(user_id, text=phrases.enter_your_programming_languages,
                                   reply_markup=Keyboards.keyboard_programming_languages)

    @staticmethod
    def __processing_registration_item_programming_language(users_message: str, user_id: int):
        if users_message == phrases.do_not_specify:
            Bot.__database.set_null_users_registration_item(user_id=user_id,
                                                            item=constants.ProfileItemsIds.PROGRAMMING_LANGUAGES)
        elif users_message in phrases.programming_languages:
            Bot.__database.append_to_users_registration_item(user_id=user_id,
                                                             item=constants.ProfileItemsIds.PROGRAMMING_LANGUAGES,
                                                             value=users_message)
        elif users_message != phrases.finish_typing:
            Bot.__bot.send_message(user_id, text=phrases.select_from_the_list)

        if users_message in (phrases.do_not_specify, phrases.finish_typing):
            Bot.__database.switch_user_to_next_registration_item(user_id=user_id)
            Bot.__bot.send_message(user_id, text=phrases.enter_your_interests,
                                   reply_markup=Keyboards.keyboard_interests)

    @staticmethod
    def __processing_registration_item_interests(users_message: str, user_id: int):
        if users_message == phrases.do_not_specify:
            Bot.__database.set_null_users_registration_item(user_id=user_id,
                                                            item=constants.ProfileItemsIds.INTERESTS)
        elif users_message in phrases.interests:
            Bot.__database.append_to_users_registration_item(user_id=user_id,
                                                             item=constants.ProfileItemsIds.INTERESTS,
                                                             value=users_message)
        elif users_message != phrases.finish_typing:
            Bot.__bot.send_message(user_id, text=phrases.select_from_the_list)

        if users_message in (phrases.do_not_specify, phrases.finish_typing):
            Bot.__database.switch_user_to_next_registration_item(user_id=user_id)
            Bot.__bot.send_message(user_id, text=phrases.finish_registration,
                                   reply_markup=telebot.types.ReplyKeyboardRemove())
            Bot.__show_users_profile(user_id)
