import telebot
import phrases_ru as phrases
import constants
import keyboards

import bottoken
from database import Database

bot = telebot.TeleBot(bottoken.TOKEN, parse_mode=None)
database = Database()

keyboard_do_not_specify = keyboards.create_keyboard_do_not_specify()
keyboard_spoken_languages = keyboards.create_keyboard_with_multiple_choice(items_list=phrases.spoken_languages)
keyboard_programming_languages = keyboards.create_keyboard_with_multiple_choice(
    items_list=phrases.programming_languages)


def show_main_menu(chat_id: int):
    """Main bot menu"""
    menu = telebot.types.InlineKeyboardMarkup()  # Create inline-keyboard
    # Add all functions into menu
    for i in range(len(phrases.main_menu_list)):
        menu.add(telebot.types.InlineKeyboardButton(
            text=phrases.main_menu_list[i],
            callback_data=constants.MAIN_MENU_PREFIX + str(i)))

    bot.send_message(chat_id, text=phrases.main_menu_title, reply_markup=menu)


@bot.message_handler(commands=['main_menu'])
def main_menu(message):
    """Show main menu"""
    show_main_menu(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    """Inline-keyboards button's click handler"""

    users_active_menu_id = database.get_users_menu_id(call.message.chat.id)

    bot.answer_callback_query(callback_query_id=call.id, text='')

    if users_active_menu_id == constants.MenuIds.MAIN_MENU:
        if call.data == constants.MAIN_MENU_PREFIX + "0":
            bot.send_message(call.message.chat.id,
                             text="OK")

        elif call.data == constants.MAIN_MENU_PREFIX + "1":
            bot.send_message(call.message.chat.id,
                             text=phrases.not_ready_yet)
        elif call.data == constants.MAIN_MENU_PREFIX + "2":
            bot.send_message(call.message.chat.id,
                             text=phrases.not_ready_yet)


def check_registration(user_id):
    if database.is_registrated(user_id):
        show_main_menu(user_id)
    else:
        bot.send_message(user_id, text=phrases.user_not_registered_yet)
        bot.send_message(user_id, text=phrases.enter_your_first_name,
                         reply_markup=keyboard_do_not_specify)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     text=phrases.welcome_message,
                     reply_markup=telebot.types.ReplyKeyboardRemove())

    check_registration(message.chat.id)


@bot.message_handler(content_types=["text"])
def processing_all_text_messages(message):
    users_message = message.text

    users_menu_id = database.get_users_menu_id(telegram_id=message.chat.id)
    users_registration_item_id = database.get_users_registration_item_id(telegram_id=message.chat.id)

    if users_menu_id == constants.MenuIds.REGISTRATION_MENU:
        if users_registration_item_id == constants.RegistationItemsIds.FIRST_NAME:
            if users_message == phrases.do_not_specify:
                database.write_empty_users_registration_item(telegram_id=message.chat.id,
                                                             item=constants.RegistationItemsIds.FIRST_NAME)
            else:
                database.write_users_registration_item(telegram_id=message.chat.id,
                                                       item=constants.RegistationItemsIds.FIRST_NAME,
                                                       value=users_message)

            database.switch_user_to_next_registration_item(telegram_id=message.chat.id)
            bot.send_message(message.chat.id, text=phrases.enter_your_last_name)

        elif users_registration_item_id == constants.RegistationItemsIds.LAST_NAME:
            if users_message == phrases.do_not_specify:
                database.write_empty_users_registration_item(telegram_id=message.chat.id,
                                                             item=constants.RegistationItemsIds.LAST_NAME)
            else:
                database.write_users_registration_item(telegram_id=message.chat.id,
                                                       item=constants.RegistationItemsIds.LAST_NAME,
                                                       value=users_message)

            database.switch_user_to_next_registration_item(telegram_id=message.chat.id)
            bot.send_message(message.chat.id, text=phrases.enter_your_age)

        elif users_registration_item_id == constants.RegistationItemsIds.AGE:
            if users_message == phrases.do_not_specify:
                database.write_empty_users_registration_item(telegram_id=message.chat.id,
                                                             item=constants.RegistationItemsIds.AGE)
            else:
                database.write_users_registration_item(telegram_id=message.chat.id,
                                                       item=constants.RegistationItemsIds.AGE,
                                                       value=users_message)

            database.switch_user_to_next_registration_item(telegram_id=message.chat.id)
            bot.send_message(message.chat.id, text=phrases.enter_your_spoken_languages,
                             reply_markup=keyboard_spoken_languages)

        elif users_registration_item_id == constants.RegistationItemsIds.SPOKEN_LANGUAGES:
            if users_message == phrases.do_not_specify:
                database.write_empty_users_registration_item(telegram_id=message.chat.id,
                                                             item=constants.RegistationItemsIds.SPOKEN_LANGUAGES)
            elif users_message == phrases.finish_typing:
                database.switch_user_to_next_registration_item(telegram_id=message.chat.id)
                bot.send_message(message.chat.id, text=phrases.enter_your_programming_languages,
                                 reply_markup=keyboard_programming_languages)
            else:
                database.write_users_registration_item(telegram_id=message.chat.id,
                                                       item=constants.RegistationItemsIds.SPOKEN_LANGUAGES,
                                                       value=users_message)

        elif users_registration_item_id == constants.RegistationItemsIds.PROGRAMMING_LANGUAGES:
            if users_message == phrases.do_not_specify:
                database.write_empty_users_registration_item(telegram_id=message.chat.id,
                                                             item=constants.RegistationItemsIds.PROGRAMMING_LANGUAGES)
            elif users_message == phrases.finish_typing:
                database.switch_user_to_next_registration_item(telegram_id=message.chat.id)
                bot.send_message(message.chat.id, text=phrases.enter_your_interests,
                                 reply_markup=keyboard_programming_languages)
            else:
                database.write_users_registration_item(telegram_id=message.chat.id,
                                                       item=constants.RegistationItemsIds.PROGRAMMING_LANGUAGES,
                                                       value=users_message)

    else:
        bot.send_message(message.chat.id, text="Bla-bla-bla")


if __name__ == '__main__':  # Run
    bot.polling(none_stop=True)
