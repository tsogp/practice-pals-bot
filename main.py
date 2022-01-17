import telebot
import phrases_ru as phrases
import constants

import bottoken
from database import Database

bot = telebot.TeleBot(bottoken.TOKEN, parse_mode=None)
database = Database()

keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2,
                                             resize_keyboard=True)
keyboard.add(telebot.types.KeyboardButton(text=phrases.do_not_specify))


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

    if users_active_menu_id == constants.MAIN_MENU_ID:
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
                         reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     text=phrases.welcome_message,
                     reply_markup=telebot.types.ReplyKeyboardRemove())

    check_registration(message.chat.id)


@bot.message_handler(content_types=["text"])
def processing_all_text_messages(message):
    users_message = message.text

    if database.get_users_menu_id(telegram_id=message.chat.id) == constants.REGISTRATION_MENU_ID:
        if database.get_users_registration_point_id(telegram_id=message.chat.id) == constants.REGISTRATION_ITEM_NAME:
            if users_message == phrases.do_not_specify:
                database.write_empty_users_registration_item(telegram_id=message.chat.id,
                                                             item=constants.REGISTRATION_ITEM_NAME)
            else:
                database.write_users_registration_item(telegram_id=message.chat.id,
                                                       item=constants.REGISTRATION_ITEM_NAME,
                                                       value=users_message)
            database.switch_user_to_next_registration_item(telegram_id=message.chat.id)
            bot.send_message(message.chat.id, text=phrases.enter_your_last_name)
    else:
        bot.send_message(message.chat.id, text="Bla-bla-bla")


if __name__ == '__main__':  # Run
    bot.polling(none_stop=True)
