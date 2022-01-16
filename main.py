import telebot
import phrases_ru as phrases

import bottoken

bot = telebot.TeleBot(bottoken.TOKEN, parse_mode=None)


def main_menu(chat_id):
    """Main bot_menu"""
    menu = telebot.types.InlineKeyboardMarkup()  # Create inline-keyboard
    # Add all functions into menu
    for i in range(len(phrases.main_menu_list)):
        menu.add(telebot.types.InlineKeyboardButton(
            text=phrases.main_menu_list[i],
            callback_data=f'main_menu_{i + 1}'))

    bot.send_message(chat_id, text=phrases.main_menu_title, reply_markup=menu)


@bot.message_handler(commands=['menu'])
def menu(message):
    """Show main menu"""
    main_menu(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    """Inline-keyboards button's click handler"""
    bot.answer_callback_query(callback_query_id=call.id, text='')
    if call.data == 'main_menu_1':
        bot.send_message(call.message.chat.id,
                         text="OK")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     text=phrases.welcome_message,
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    main_menu(message.chat.id)


if __name__ == '__main__':  # Run
    bot.polling(none_stop=True)
