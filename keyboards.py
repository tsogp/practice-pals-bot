import telebot
import phrases_ru as phrases


class Keyboards:

    @staticmethod
    def __create_keyboard_do_not_specify():
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2,
                                                     resize_keyboard=True)
        keyboard.add(telebot.types.KeyboardButton(text=phrases.do_not_specify))
        return keyboard

    @staticmethod
    def __create_keyboard_with_multiple_choice(items_list: list):
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2,
                                                     resize_keyboard=True)
        for language in items_list:
            keyboard.add(telebot.types.KeyboardButton(text=language))
        keyboard.add(telebot.types.KeyboardButton(text=phrases.finish_typing))
        keyboard.add(telebot.types.KeyboardButton(text=phrases.do_not_specify))
        return keyboard

    keyboard_do_not_specify = __create_keyboard_do_not_specify()
    keyboard_spoken_languages = __create_keyboard_with_multiple_choice(items_list=phrases.spoken_languages)
    keyboard_programming_languages = __create_keyboard_with_multiple_choice(items_list=phrases.programming_languages)
    keyboard_interests = __create_keyboard_with_multiple_choice(items_list=phrases.interests)
