import telebot
import phrases_ru as phrases


class Keyboards:

    @staticmethod
    def __create_keyboard_with_one_button(button_text: str):
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keyboard.add(telebot.types.KeyboardButton(text=button_text))
        return keyboard

    @staticmethod
    def __create_keyboard_ok_edit():
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keyboard.add(telebot.types.KeyboardButton(text=phrases.ok_edit[0]),
                     telebot.types.KeyboardButton(text=phrases.ok_edit[1]))
        return keyboard

    @staticmethod
    def __create_keyboard_main_menu():
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for i in range(len(phrases.main_menu_list)):
            keyboard.add(telebot.types.KeyboardButton(text=phrases.main_menu_list[i]))
        return keyboard

    @staticmethod
    def __create_keyboard_with_multiple_choice(items_list: list, skip_button: str):
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        for i in range(0, len(items_list), 2):
            keyboard.add(telebot.types.KeyboardButton(text=items_list[i]),
                         telebot.types.KeyboardButton(text=items_list[i + 1]))
        if len(items_list) % 2 != 0:
            keyboard.add(telebot.types.KeyboardButton(text=items_list[-1]))

        keyboard.add(telebot.types.KeyboardButton(text=phrases.finish_typing))
        keyboard.add(telebot.types.KeyboardButton(text=skip_button))
        return keyboard

    profile_do_not_specify = __create_keyboard_with_one_button(phrases.do_not_specify)
    profile_spoken_languages = __create_keyboard_with_multiple_choice(items_list=phrases.spoken_languages,
                                                                      skip_button=phrases.do_not_specify)
    profile_programming_languages = __create_keyboard_with_multiple_choice(items_list=phrases.programming_languages,
                                                                           skip_button=phrases.do_not_specify)
    profile_interests = __create_keyboard_with_multiple_choice(items_list=phrases.interests,
                                                               skip_button=phrases.do_not_specify)
    profile_ok_edit = __create_keyboard_ok_edit()
    main_menu = __create_keyboard_main_menu()
    search_parameters_does_not_matter = __create_keyboard_with_one_button(phrases.does_not_matter)
    search_parameters_age_groups = __create_keyboard_with_multiple_choice(items_list=phrases.age_groups,
                                                                          skip_button=phrases.does_not_matter)
    search_parameters_spoken_languages = __create_keyboard_with_multiple_choice(items_list=phrases.spoken_languages,
                                                                                skip_button=phrases.does_not_matter)
