import telebot
import phrases_ru as phrases
import constants
from keyboards import Keyboards

import bottoken
from database import Database


class Bot:
    __bot = telebot.TeleBot(bottoken.TOKEN)
    __database = Database()

    @staticmethod
    def run():
        Bot.__bot.polling(none_stop=True)

    @staticmethod
    def __show_main_menu(chat_id: int):
        menu = telebot.types.InlineKeyboardMarkup()  # Create inline-keyboard
        # Add all functions into menu
        for i in range(len(phrases.main_menu_list)):
            menu.add(telebot.types.InlineKeyboardButton(
                text=phrases.main_menu_list[i],
                callback_data=constants.MAIN_MENU_PREFIX + str(i)))
        Bot.__bot.send_message(chat_id, text=phrases.main_menu_title, reply_markup=menu)

    @__bot.message_handler(commands=['main_menu'])
    @staticmethod
    def __main_menu(message):
        Bot.__show_main_menu(message.chat.id)

    @staticmethod
    def __check_registration(user_id):
        if Bot.__database.is_registrated(user_id):
            Bot.__show_main_menu(user_id)
        else:
            Bot.__bot.send_message(user_id, text=phrases.user_not_registered_yet)
            Bot.__bot.send_message(user_id, text=phrases.enter_your_first_name,
                                   reply_markup=Keyboards.keyboard_do_not_specify)

    @staticmethod
    def __show_users_profile(user_id):
        profile_str = ""
        profile_str += (f"*{phrases.profile_items[0]}:* " +
                        Bot.__database.get_users_profile_item(user_id, constants.RegistationItemsIds.FIRST_NAME) + "\n")
        profile_str += (f"*{phrases.profile_items[1]}:* " +
                        Bot.__database.get_users_profile_item(user_id, constants.RegistationItemsIds.LAST_NAME) + "\n")
        profile_str += (f"*{phrases.profile_items[2]}:* " +
                        Bot.__database.get_users_profile_item(user_id, constants.RegistationItemsIds.AGE) + "\n")
        profile_str += (f"*{phrases.profile_items[3]}:* " +
                        Bot.__database.get_users_profile_item(user_id,
                                                              constants.RegistationItemsIds.SPOKEN_LANGUAGES) + "\n")
        profile_str += (f"*{phrases.profile_items[4]}:* " +
                        Bot.__database.get_users_profile_item(user_id,
                                                              constants.RegistationItemsIds.PROGRAMMING_LANGUAGES) + "\n")
        profile_str += (f"*{phrases.profile_items[5]}:* " +
                        Bot.__database.get_users_profile_item(user_id, constants.RegistationItemsIds.INTERESTS) + "\n")
        Bot.__bot.send_message(user_id, text=phrases.your_profile)
        Bot.__bot.send_message(user_id, text=profile_str, parse_mode="Markdown",
                               reply_markup=Keyboards.keyboard_ok_edit)
        Bot.__database.set_users_menu_id(user_id, constants.MenuIds.CHECK_PROFILE_MENU)

    @__bot.callback_query_handler(func=lambda call: True)
    @staticmethod
    def __query_handler(call):
        """Inline-keyboards button's click handler"""

        users_active_menu_id = Bot.__database.get_users_menu_id(call.message.chat.id)

        Bot.__bot.answer_callback_query(callback_query_id=call.id, text='')

        if users_active_menu_id == constants.MenuIds.MAIN_MENU:
            if call.data == constants.MAIN_MENU_PREFIX + "0":
                Bot.__bot.send_message(call.message.chat.id,
                                       text="OK")

            elif call.data == constants.MAIN_MENU_PREFIX + "1":
                Bot.__bot.send_message(call.message.chat.id,
                                       text=phrases.not_ready_yet)
            elif call.data == constants.MAIN_MENU_PREFIX + "2":
                Bot.__bot.send_message(call.message.chat.id,
                                       text=phrases.not_ready_yet)

    @__bot.message_handler(commands=['start'])
    @staticmethod
    def start(message):
        Bot.__bot.send_message(message.chat.id,
                               text=phrases.welcome_message,
                               reply_markup=telebot.types.ReplyKeyboardRemove())
        Bot.__check_registration(message.chat.id)

    @__bot.message_handler(content_types=["text"])
    @staticmethod
    def __processing_all_text_messages(message):
        users_message = message.text

        users_menu_id = Bot.__database.get_users_menu_id(telegram_id=message.chat.id)
        users_registration_item_id = Bot.__database.get_users_registration_item_id(telegram_id=message.chat.id)

        if users_menu_id == constants.MenuIds.REGISTRATION_MENU:
            if users_registration_item_id == constants.RegistationItemsIds.FIRST_NAME:
                Bot.__processing_registration_item_first_name(users_message, chat_id=message.chat.id)
            elif users_registration_item_id == constants.RegistationItemsIds.LAST_NAME:
                Bot.__processing_registration_item_last_name(users_message, chat_id=message.chat.id)
            elif users_registration_item_id == constants.RegistationItemsIds.AGE:
                Bot.__processing_registration_item_age(users_message, chat_id=message.chat.id)
            elif users_registration_item_id == constants.RegistationItemsIds.SPOKEN_LANGUAGES:
                Bot.__processing_registration_item_spoken_language(users_message, chat_id=message.chat.id)
            elif users_registration_item_id == constants.RegistationItemsIds.PROGRAMMING_LANGUAGES:
                Bot.__processing_registration_item_programming_language(users_message, chat_id=message.chat.id)
            elif users_registration_item_id == constants.RegistationItemsIds.INTERESTS:
                Bot.__processing_registration_item_interests(users_message, chat_id=message.chat.id)
        elif users_menu_id == constants.MenuIds.CHECK_PROFILE_MENU:
            print(1)
            if users_message == phrases.ok_edit[0]:
                Bot.__database.set_users_menu_id(message.chat.id, constants.MenuIds.MAIN_MENU)
                Bot.__show_main_menu(message.chat.id)
                print(2)
            elif users_message == phrases.ok_edit[1]:
                Bot.__bot.send_message(message.chat.id, text=phrases.not_ready_yet)
                Bot.__database.set_users_menu_id(message.chat.id, constants.MenuIds.MAIN_MENU)
                Bot.__show_main_menu(message.chat.id)
                print(3)
        else:
            Bot.__bot.send_message(message.chat.id, text="Bla-bla-bla")

    @staticmethod
    def __processing_registration_item_first_name(users_message, chat_id):
        if users_message == phrases.do_not_specify:
            Bot.__database.set_null_users_registration_item(telegram_id=chat_id,
                                                            item=constants.RegistationItemsIds.FIRST_NAME)
        else:
            Bot.__database.set_users_registration_item(telegram_id=chat_id,
                                                       item=constants.RegistationItemsIds.FIRST_NAME,
                                                       value=users_message)

        Bot.__database.switch_user_to_next_registration_item(telegram_id=chat_id)
        Bot.__bot.send_message(chat_id, text=phrases.enter_your_last_name)

    @staticmethod
    def __processing_registration_item_last_name(users_message, chat_id):
        if users_message == phrases.do_not_specify:
            Bot.__database.set_null_users_registration_item(telegram_id=chat_id,
                                                            item=constants.RegistationItemsIds.LAST_NAME)
        else:
            Bot.__database.set_users_registration_item(telegram_id=chat_id,
                                                       item=constants.RegistationItemsIds.LAST_NAME,
                                                       value=users_message)

        Bot.__database.switch_user_to_next_registration_item(telegram_id=chat_id)
        Bot.__bot.send_message(chat_id, text=phrases.enter_your_age)

    @staticmethod
    def __processing_registration_item_age(users_message, chat_id):
        if users_message == phrases.do_not_specify:
            Bot.__database.set_null_users_registration_item(telegram_id=chat_id,
                                                            item=constants.RegistationItemsIds.AGE)
        else:
            Bot.__database.set_users_registration_item(telegram_id=chat_id,
                                                       item=constants.RegistationItemsIds.AGE,
                                                       value=users_message)

        Bot.__database.switch_user_to_next_registration_item(telegram_id=chat_id)
        Bot.__bot.send_message(chat_id, text=phrases.enter_your_spoken_languages,
                               reply_markup=Keyboards.keyboard_spoken_languages)

    @staticmethod
    def __processing_registration_item_spoken_language(users_message, chat_id):
        if users_message == phrases.do_not_specify:
            Bot.__database.set_null_users_registration_item(telegram_id=chat_id,
                                                            item=constants.RegistationItemsIds.SPOKEN_LANGUAGES)
        elif users_message != phrases.finish_typing:
            Bot.__database.append_to_users_registration_item(telegram_id=chat_id,
                                                             item=constants.RegistationItemsIds.SPOKEN_LANGUAGES,
                                                             value=users_message)

        if users_message in (phrases.do_not_specify, phrases.finish_typing):
            Bot.__database.switch_user_to_next_registration_item(telegram_id=chat_id)
            Bot.__bot.send_message(chat_id, text=phrases.enter_your_programming_languages,
                                   reply_markup=Keyboards.keyboard_programming_languages)

    @staticmethod
    def __processing_registration_item_programming_language(users_message, chat_id):
        if users_message == phrases.do_not_specify:
            Bot.__database.set_null_users_registration_item(telegram_id=chat_id,
                                                            item=constants.RegistationItemsIds.PROGRAMMING_LANGUAGES)
        elif users_message != phrases.finish_typing:
            Bot.__database.append_to_users_registration_item(telegram_id=chat_id,
                                                             item=constants.RegistationItemsIds.PROGRAMMING_LANGUAGES,
                                                             value=users_message)

        if users_message in (phrases.do_not_specify, phrases.finish_typing):
            Bot.__database.switch_user_to_next_registration_item(telegram_id=chat_id)
            Bot.__bot.send_message(chat_id, text=phrases.enter_your_interests,
                                   reply_markup=Keyboards.keyboard_interests)

    @staticmethod
    def __processing_registration_item_interests(users_message, chat_id):
        if users_message == phrases.do_not_specify:
            Bot.__database.set_null_users_registration_item(telegram_id=chat_id,
                                                            item=constants.RegistationItemsIds.INTERESTS)
        elif users_message != phrases.finish_typing:
            Bot.__database.append_to_users_registration_item(telegram_id=chat_id,
                                                             item=constants.RegistationItemsIds.INTERESTS,
                                                             value=users_message)

        if users_message in (phrases.do_not_specify, phrases.finish_typing):
            Bot.__database.switch_user_to_next_registration_item(telegram_id=chat_id)
            Bot.__bot.send_message(chat_id, text=phrases.finish_registration,
                                   reply_markup=telebot.types.ReplyKeyboardRemove())
            Bot.__show_users_profile(chat_id)
            # print(Bot.__database.data)
