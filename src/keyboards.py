# File with telegram's keyboards objects for bot
import telebot

import constants
import phrases_ru as phrases
from typing import Type, Optional, List


class Keyboards:

    @staticmethod
    def __create_keyboard_with_one_button(button_text: str):
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keyboard.add(telebot.types.KeyboardButton(text=button_text))
        return keyboard

    @staticmethod
    def __create_keyboard_ok_edit(ok: str, edit: str):
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keyboard.add(telebot.types.KeyboardButton(text=ok),
                     telebot.types.KeyboardButton(text=edit))
        return keyboard

    @staticmethod
    def __create_menu_from_list(items_list):
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for item in items_list:
            keyboard.add(telebot.types.KeyboardButton(text=item))
        return keyboard

    @staticmethod
    def __create_menu_from_list_width_2(items_list):
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        for i in range(0, len(items_list) - 1, 2):
            keyboard.add(telebot.types.KeyboardButton(text=items_list[i]),
                         telebot.types.KeyboardButton(text=items_list[i + 1]))
        if len(items_list) % 2 != 0:
            keyboard.add(telebot.types.KeyboardButton(text=items_list[-1]))
        return keyboard

    @staticmethod
    def __create_keyboard_with_multiple_choice(items_list: list, skip_button: str):
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        for i in range(0, len(items_list) - 1, 2):
            keyboard.add(telebot.types.KeyboardButton(text=items_list[i]),
                         telebot.types.KeyboardButton(text=items_list[i + 1]))
        if len(items_list) % 2 != 0:
            keyboard.add(telebot.types.KeyboardButton(text=items_list[-1]))

        keyboard.add(telebot.types.KeyboardButton(text=phrases.finish_typing))
        keyboard.add(telebot.types.KeyboardButton(text=skip_button))
        return keyboard

    @staticmethod
    def __create_inline_button(text_value: str, source_value: str):
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)  # Create inline-keyboard
        keyboard.add(telebot.types.InlineKeyboardButton(
            text=text_value,
            callback_data=source_value))
        return keyboard

    @staticmethod
    def __create_inline_keyboard_from_list(items_list: Type[constants.Items], dictionary: dict):
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)  # Create inline-keyboard
        for item in list(items_list):
            keyboard.add(telebot.types.InlineKeyboardButton(
                text=item.get_str_value(dictionary),
                callback_data=item.get_source_value()))
        return keyboard

    @staticmethod
    def __create_btn_with_link(text: str, link: str):
        keyboard = telebot.types.InlineKeyboardMarkup()
        btn_my_site = telebot.types.InlineKeyboardButton(text=text, url=link)
        keyboard.add(btn_my_site)
        return keyboard

    @staticmethod
    def create_inline_keyboard_with_multiple_choice(field: Type[constants.Items],
                                                    active_items: Optional[List[constants.Items]],
                                                    dictionary: dict):
        if active_items is None:
            active_items = []
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)  # Create inline-keyboard
        for item in field:
            btn_text = ("\U00002705 " if item in active_items else "") + item.get_str_value(dictionary)
            keyboard.add(telebot.types.InlineKeyboardButton(
                text=btn_text,
                callback_data=item.get_source_value()))
        return keyboard

    profile_do_not_specify = __create_keyboard_with_one_button(phrases.do_not_specify)
    profile_finish_and_skip = __create_keyboard_with_multiple_choice(items_list=[], skip_button=phrases.do_not_specify)
    profile_ok_edit = __create_keyboard_ok_edit(phrases.ok_edit[0], phrases.ok_edit[1])
    main_menu = __create_menu_from_list_width_2(
        constants.MainMenuItems.get_all_str_vales(phrases.values_of_main_menu_items))
    search_parameters_does_not_matter = __create_keyboard_with_one_button(phrases.does_not_matter)
    search_parameters_finish_and_skip = __create_keyboard_with_multiple_choice(items_list=[],
                                                                               skip_button=phrases.does_not_matter)
    search_parameters_ok_edit = __create_keyboard_ok_edit(phrases.ok_edit[0], phrases.ok_edit[1])
    search_menu = __create_menu_from_list_width_2(
        constants.SearchMenuItems.get_all_str_vales(phrases.values_of_search_menu_items))

    profile_reaction_menu = __create_inline_keyboard_from_list(constants.ProfileReactionsMenu,
                                                               phrases.profile_reaction_menu_items)

    subscription_menu = __create_menu_from_list(items_list=[phrases.paid])

    go_to_subscription_menu_btn = __create_inline_button(phrases.go_to_subscription_menu,
                                                         constants.GO_TO_SUBSCRIPTION_MENU)

    button_for_payment = __create_btn_with_link(phrases.buy, constants.link_to_yoomoney)

    ask_personal_data = __create_inline_keyboard_from_list(constants.AskPersonalData,
                                                           phrases.ask_personal_data_menu_items)
