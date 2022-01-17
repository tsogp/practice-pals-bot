import telebot
import phrases_ru as phrases


def create_keyboard_do_not_specify():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2,
                                                 resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton(text=phrases.do_not_specify))
    return keyboard


def create_keyboard_with_multiple_choice(items_list: list):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2,
                                                 resize_keyboard=True)
    for language in items_list:
        keyboard.add(telebot.types.KeyboardButton(text=language))
    keyboard.add(telebot.types.KeyboardButton(text=phrases.finish_typing))
    keyboard.add(telebot.types.KeyboardButton(text=phrases.do_not_specify))
    return keyboard
