import telebot
import phrases_ru as phrases
import constants
import keyboards

import bottoken
from database import Database


class Bot:
    bot = telebot.TeleBot(bottoken.TOKEN)
    database = Database()

    keyboard_do_not_specify = keyboards.create_keyboard_do_not_specify()
    keyboard_spoken_languages = keyboards.create_keyboard_with_multiple_choice(items_list=phrases.spoken_languages)
    keyboard_programming_languages = keyboards.create_keyboard_with_multiple_choice(
        items_list=phrases.programming_languages)
    keyboard_interests = keyboards.create_keyboard_with_multiple_choice(items_list=phrases.interests)

    @staticmethod
    def run():
        Bot.bot.polling(none_stop=True)

    @staticmethod
    def show_main_menu(chat_id: int):
        """Main bot menu"""
        menu = telebot.types.InlineKeyboardMarkup()  # Create inline-keyboard
        # Add all functions into menu
        for i in range(len(phrases.main_menu_list)):
            menu.add(telebot.types.InlineKeyboardButton(
                text=phrases.main_menu_list[i],
                callback_data=constants.MAIN_MENU_PREFIX + str(i)))

        Bot.bot.send_message(chat_id, text=phrases.main_menu_title, reply_markup=menu)

    @bot.message_handler(commands=['main_menu'])
    @staticmethod
    def main_menu(message):
        """Show main menu"""
        Bot.show_main_menu(message.chat.id)

    @staticmethod
    def check_registration(user_id):
        if Bot.database.is_registrated(user_id):
            Bot.show_main_menu(user_id)
        else:
            Bot.bot.send_message(user_id, text=phrases.user_not_registered_yet)
            Bot.bot.send_message(user_id, text=phrases.enter_your_first_name,
                                 reply_markup=Bot.keyboard_do_not_specify)

    @bot.callback_query_handler(func=lambda call: True)
    @staticmethod
    def query_handler(call):
        """Inline-keyboards button's click handler"""

        users_active_menu_id = Bot.database.get_users_menu_id(call.message.chat.id)

        Bot.bot.answer_callback_query(callback_query_id=call.id, text='')

        if users_active_menu_id == constants.MenuIds.MAIN_MENU:
            if call.data == constants.MAIN_MENU_PREFIX + "0":
                Bot.bot.send_message(call.message.chat.id,
                                     text="OK")

            elif call.data == constants.MAIN_MENU_PREFIX + "1":
                Bot.bot.send_message(call.message.chat.id,
                                     text=phrases.not_ready_yet)
            elif call.data == constants.MAIN_MENU_PREFIX + "2":
                Bot.bot.send_message(call.message.chat.id,
                                     text=phrases.not_ready_yet)

    @bot.message_handler(commands=['start'])
    @staticmethod
    def start(message):
        Bot.bot.send_message(message.chat.id,
                             text=phrases.welcome_message,
                             reply_markup=telebot.types.ReplyKeyboardRemove())

        Bot.check_registration(message.chat.id)

    @bot.message_handler(content_types=["text"])
    @staticmethod
    def processing_all_text_messages(message):
        users_message = message.text

        users_menu_id = Bot.database.get_users_menu_id(telegram_id=message.chat.id)
        users_registration_item_id = Bot.database.get_users_registration_item_id(telegram_id=message.chat.id)

        if users_menu_id == constants.MenuIds.REGISTRATION_MENU:
            if users_registration_item_id == constants.RegistationItemsIds.FIRST_NAME:
                if users_message == phrases.do_not_specify:
                    Bot.database.write_empty_users_registration_item(telegram_id=message.chat.id,
                                                                     item=constants.RegistationItemsIds.FIRST_NAME)
                else:
                    Bot.database.write_users_registration_item(telegram_id=message.chat.id,
                                                               item=constants.RegistationItemsIds.FIRST_NAME,
                                                               value=users_message)

                Bot.database.switch_user_to_next_registration_item(telegram_id=message.chat.id)
                Bot.bot.send_message(message.chat.id, text=phrases.enter_your_last_name)

            elif users_registration_item_id == constants.RegistationItemsIds.LAST_NAME:
                if users_message == phrases.do_not_specify:
                    Bot.database.write_empty_users_registration_item(telegram_id=message.chat.id,
                                                                     item=constants.RegistationItemsIds.LAST_NAME)
                else:
                    Bot.database.write_users_registration_item(telegram_id=message.chat.id,
                                                               item=constants.RegistationItemsIds.LAST_NAME,
                                                               value=users_message)

                Bot.database.switch_user_to_next_registration_item(telegram_id=message.chat.id)
                Bot.bot.send_message(message.chat.id, text=phrases.enter_your_age)

            elif users_registration_item_id == constants.RegistationItemsIds.AGE:
                if users_message == phrases.do_not_specify:
                    Bot.database.write_empty_users_registration_item(telegram_id=message.chat.id,
                                                                     item=constants.RegistationItemsIds.AGE)
                else:
                    Bot.database.write_users_registration_item(telegram_id=message.chat.id,
                                                               item=constants.RegistationItemsIds.AGE,
                                                               value=users_message)

                Bot.database.switch_user_to_next_registration_item(telegram_id=message.chat.id)
                Bot.bot.send_message(message.chat.id, text=phrases.enter_your_spoken_languages,
                                     reply_markup=Bot.keyboard_spoken_languages)

            elif users_registration_item_id == constants.RegistationItemsIds.SPOKEN_LANGUAGES:
                if users_message == phrases.do_not_specify:
                    Bot.database.write_empty_users_registration_item(telegram_id=message.chat.id,
                                                                     item=constants.RegistationItemsIds.SPOKEN_LANGUAGES)
                elif users_message != phrases.finish_typing:
                    Bot.database.write_users_registration_item(telegram_id=message.chat.id,
                                                               item=constants.RegistationItemsIds.SPOKEN_LANGUAGES,
                                                               value=users_message)

                if users_message in (phrases.do_not_specify, phrases.finish_typing):
                    Bot.database.switch_user_to_next_registration_item(telegram_id=message.chat.id)
                    Bot.bot.send_message(message.chat.id, text=phrases.enter_your_programming_languages,
                                         reply_markup=Bot.keyboard_programming_languages)

            elif users_registration_item_id == constants.RegistationItemsIds.PROGRAMMING_LANGUAGES:
                if users_message == phrases.do_not_specify:
                    Bot.database.write_empty_users_registration_item(telegram_id=message.chat.id,
                                                                     item=constants.RegistationItemsIds.PROGRAMMING_LANGUAGES)
                elif users_message != phrases.finish_typing:
                    Bot.database.write_users_registration_item(telegram_id=message.chat.id,
                                                               item=constants.RegistationItemsIds.PROGRAMMING_LANGUAGES,
                                                               value=users_message)

                if users_message in (phrases.do_not_specify, phrases.finish_typing):
                    Bot.database.switch_user_to_next_registration_item(telegram_id=message.chat.id)
                    Bot.bot.send_message(message.chat.id, text=phrases.enter_your_interests,
                                         reply_markup=Bot.keyboard_interests)

            elif users_registration_item_id == constants.RegistationItemsIds.INTERESTS:
                if users_message == phrases.do_not_specify:
                    Bot.database.write_empty_users_registration_item(telegram_id=message.chat.id,
                                                                     item=constants.RegistationItemsIds.INTERESTS)
                elif users_message != phrases.finish_typing:
                    Bot.database.write_users_registration_item(telegram_id=message.chat.id,
                                                               item=constants.RegistationItemsIds.INTERESTS,
                                                               value=users_message)

                if users_message in (phrases.do_not_specify, phrases.finish_typing):
                    Bot.database.switch_user_to_next_registration_item(telegram_id=message.chat.id)
                    Bot.bot.send_message(message.chat.id, text=phrases.finish_registration,
                                         reply_markup=telebot.types.ReplyKeyboardRemove())

        else:
            Bot.bot.send_message(message.chat.id, text="Bla-bla-bla")
