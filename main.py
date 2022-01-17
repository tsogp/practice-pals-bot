import telebot
import phrases_ru as phrases
import constants

import bottoken
from database import Database

bot = telebot.TeleBot(bottoken.TOKEN, parse_mode=None)
database = Database()


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

    users_active_menu_id = database.get_users_menu_id_by_telegram_id(call.message.chat.id)

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


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     text=phrases.welcome_message,
                     reply_markup=telebot.types.ReplyKeyboardRemove())

    check_registration(message.chat.id)


if __name__ == '__main__':  # Run
    bot.polling(none_stop=True)
