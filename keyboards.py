import telebot
import phrases_ru as phrases


class Keyboards:

    @staticmethod
    def __create_keyboard_do_not_specify():
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keyboard.add(telebot.types.KeyboardButton(text=phrases.do_not_specify))
        return keyboard

    @staticmethod
    def __create_keyboard_with_multiple_choice(items_list: list):
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        for i in range(0, len(items_list), 2):
            keyboard.add(telebot.types.KeyboardButton(text=items_list[i]),
                         telebot.types.KeyboardButton(text=items_list[i + 1]))
        if len(items_list) % 2 != 0:
            keyboard.add(telebot.types.KeyboardButton(text=items_list[-1]))

        keyboard.add(telebot.types.KeyboardButton(text=phrases.finish_typing))
        keyboard.add(telebot.types.KeyboardButton(text=phrases.do_not_specify))
        return keyboard

    keyboard_do_not_specify = __create_keyboard_do_not_specify()
    keyboard_spoken_languages = __create_keyboard_with_multiple_choice(items_list=phrases.spoken_languages)
    keyboard_programming_languages = __create_keyboard_with_multiple_choice(items_list=phrases.programming_languages)
    keyboard_interests = __create_keyboard_with_multiple_choice(items_list=phrases.interests)
