import telebot
import os

import phrases_en as phrases
import constants
from keyboards import Keyboards
import config
from typing import Type

from IDatabase import IDatabase
from RealDatabase import Database
from flask import Flask, request
import logging

from User import User

bot = telebot.TeleBot(config.TOKEN)  # Telegram bot object
server = Flask(__name__)
database: IDatabase = Database()
User.set_database(database)

@server.route('/' + config.TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://practice-pals.herokuapp.com/' + config.TOKEN)
    return "!", 200

def run_bot() -> None:
    """
    Call to run bot
    """
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


@bot.message_handler(commands=['start'])
def start(message):
    """
    Processing the command "/start"
    """
    if not database.is_in_database(message.chat.id):
        database.initial_user_setup(message.chat.id)
        database.set_users_telegram_login(message.chat.id, message.from_user.username)
    bot.send_message(message.chat.id,
                     text=phrases.welcome_message,
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    check_registration(message.chat.id)


@bot.message_handler(commands=['main_menu'])
def main_menu(message):
    """
    Processing the command "/main_menu"
    """
    check_registration(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    """Inline-keyboards button's click handler"""
    users_active_menu_id = database.get_users_menu_id(call.message.chat.id)
    users_registration_item_id = database.get_users_registration_item_id(call.message.chat.id)
    users_search_parameter_item_id = database.get_users_search_parameter_item_id(call.message.chat.id)
    bot.answer_callback_query(callback_query_id=call.id, text='')

    if users_active_menu_id == constants.MenuIds.PROFILE_REACTIONS_MENU:
        if call.data == constants.ProfileReactionsMenu.LIKE.get_source_value():
            processing_like_button(call.message.chat.id)
        elif call.data == constants.ProfileReactionsMenu.SKIP.get_source_value():
            show_candidates_profile(call.message.chat.id)
        elif call.data == constants.ProfileReactionsMenu.GO_TO_MAIN_MENU.get_source_value():
            activate_main_menu(call.message.chat.id)
        elif call.data == constants.GO_TO_SUBSCRIPTION_MENU:
            activate_subscription_menu(call.message.chat.id)

    elif users_active_menu_id == constants.MenuIds.PERSONAL_DATA_MENU:
        if call.data == constants.AskPersonalData.AGREE.get_source_value():
            processing_personal_data_agree(call.message.chat.id)
        elif call.data == constants.AskPersonalData.REFUSE.get_source_value():
            processing_personal_data_refuse(call.message.chat.id)

    elif users_active_menu_id in (constants.MenuIds.REGISTRATION_MENU, constants.MenuIds.EDIT_PROFILE_MENU):
        if users_registration_item_id == constants.ProfileItemsIds.SPOKEN_LANGUAGES:
            processing_profile_item_inline(call, constants.SpokenLanguages)
        elif users_registration_item_id == constants.ProfileItemsIds.PROGRAMMING_LANGUAGES:
            processing_profile_item_inline(call, constants.ProgrammingLanguages)
        elif users_registration_item_id == constants.ProfileItemsIds.INTERESTS:
            processing_profile_item_inline(call, constants.Interests)

    elif users_active_menu_id in (
            constants.MenuIds.SEARCH_PARAMETERS_MENU, constants.MenuIds.EDIT_SEARCH_PARAMETERS_MENU):
        if users_search_parameter_item_id == constants.SearchParametersItemsIds.AGE_GROUP:
            processing_search_parameters_item_inline(call, constants.AgeGroups)
        elif users_search_parameter_item_id == constants.SearchParametersItemsIds.SPOKEN_LANGUAGES:
            processing_search_parameters_item_inline(call, constants.SpokenLanguages)
        elif users_search_parameter_item_id == constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES:
            processing_search_parameters_item_inline(call, constants.ProgrammingLanguages)
        elif users_search_parameter_item_id == constants.SearchParametersItemsIds.INTERESTS:
            processing_search_parameters_item_inline(call, constants.Interests)

    elif users_active_menu_id == constants.MenuIds.SELECT_PROFILE_ITEM_TO_EDIT_MENU:
        database.set_users_menu_id(call.message.chat.id, constants.MenuIds.EDIT_PROFILE_MENU)
        if call.data == str(constants.ProfileItemsIds.FIRST_NAME.get_source_value()):
            ask_profile_first_name(call.message.chat.id)
        elif call.data == str(constants.ProfileItemsIds.LAST_NAME.get_source_value()):
            ask_profile_last_name(call.message.chat.id)
        elif call.data == str(constants.ProfileItemsIds.AGE.get_source_value()):
            ask_profile_age(call.message.chat.id)
        elif call.data == str(constants.ProfileItemsIds.SPOKEN_LANGUAGES.get_source_value()):
            ask_profile_spoken_languages(call.message.chat.id)
        elif call.data == str(constants.ProfileItemsIds.PROGRAMMING_LANGUAGES.get_source_value()):
            ask_profile_programming_languages(call.message.chat.id)
        elif call.data == str(constants.ProfileItemsIds.INTERESTS.get_source_value()):
            ask_profile_interests(call.message.chat.id)

    elif users_active_menu_id == constants.MenuIds.SELECT_SEARCH_PARAMETERS_ITEM_TO_EDIT_MENU:
        database.set_users_menu_id(call.message.chat.id, constants.MenuIds.EDIT_SEARCH_PARAMETERS_MENU)
        if call.data == str(constants.SearchParametersItemsIds.AGE_GROUP.get_source_value()):
            ask_search_parameters_age_groups(call.message.chat.id)
        elif call.data == str(constants.SearchParametersItemsIds.SPOKEN_LANGUAGES.get_source_value()):
            ask_search_parameters_spoken_languages(call.message.chat.id)
        elif call.data == str(constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES.get_source_value()):
            ask_search_parameters_programming_languages(call.message.chat.id)
        elif call.data == str(constants.SearchParametersItemsIds.INTERESTS.get_source_value()):
            ask_search_parameters_interests(call.message.chat.id)


def processing_like_button(user_id: int):
    candidate_id = database.get_users_last_shown_profile_id(user_id)
    if candidate_id is None:
        return

    if User(user_id).is_like_acceptable():
        candidate_login = database.get_users_telegram_login_by_id(candidate_id)
        if candidate_login is None:
            msg_with_login = phrases.telegram_login + "_" + phrases.item_is_not_specified + "_"
        else:
            msg_with_login = phrases.telegram_login + "@" + candidate_login
        bot.send_message(user_id, text=msg_with_login, parse_mode="Markdown")

        database.inc_number_of_likes(user_id)
    else:
        bot.send_message(user_id, text=phrases.likes_blocked, reply_markup=Keyboards.go_to_subscription_menu_btn)

    database.set_users_last_shown_profile_id(user_id, None)


def processing_personal_data_agree(user_id):
    bot.send_message(user_id, text=phrases.personal_data_you_agree)
    bot.send_message(user_id, text=phrases.user_not_registered_yet)

    database.set_users_menu_id(user_id, constants.MenuIds.REGISTRATION_MENU)
    ask_profile_first_name(user_id)


def processing_personal_data_refuse(user_id):
    bot.send_message(user_id, text=phrases.personal_data_you_refuse)
    bot.send_message(user_id, text=phrases.user_not_registered_yet)
    database.set_users_menu_id(user_id, constants.MenuIds.REGISTRATION_MENU)
    ask_profile_spoken_languages(user_id)


def processing_profile_item_inline(call, field: Type[constants.Items]):
    item = field.get_object_by_source_value(call.data)

    if field == constants.SpokenLanguages:
        getter = database.get_users_profile_spoken_languages
        deleter = database.remove_from_users_profile_spoken_languages
        appender = database.append_to_users_profile_spoken_languages
        phrase = phrases.enter_your_spoken_languages
    elif field == constants.ProgrammingLanguages:
        getter = database.get_users_profile_programming_languages
        deleter = database.remove_from_users_profile_programming_languages
        appender = database.append_to_users_profile_programming_languages
        phrase = phrases.enter_your_programming_languages
    elif field == constants.Interests:
        getter = database.get_users_profile_interests
        deleter = database.remove_from_users_profile_interests
        appender = database.append_to_users_profile_interests
        phrase = phrases.enter_your_interests
    else:
        getter = deleter = appender = phrase = None

    user_items = getter(call.message.chat.id)
    user_items = [] if user_items is None else user_items
    if item in user_items:
        deleter(call.message.chat.id, item)
    else:
        appender(call.message.chat.id, item)

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=phrase,
                          reply_markup=Keyboards.create_inline_keyboard_with_multiple_choice(
                              field,
                              getter(call.message.chat.id),
                              phrases.values_of_possible_answers))


def processing_search_parameters_item_inline(call, field: Type[constants.Items]):
    item = field.get_object_by_source_value(call.data)

    if field == constants.AgeGroups:
        getter = database.get_users_search_parameters_age_groups
        deleter = database.remove_from_users_search_parameters_age_groups
        appender = database.append_to_users_search_parameters_age_groups
        phrase = phrases.enter_age_group_for_search
    elif field == constants.SpokenLanguages:
        getter = database.get_users_search_parameters_spoken_languages
        deleter = database.remove_from_users_search_parameters_spoken_languages
        appender = database.append_to_users_search_parameters_spoken_languages
        phrase = phrases.enter_spoken_languages
    elif field == constants.ProgrammingLanguages:
        getter = database.get_users_search_parameters_programming_languages
        deleter = database.remove_from_users_search_parameters_programming_languages
        appender = database.append_to_users_search_parameters_programming_languages
        phrase = phrases.enter_programming_languages
    elif field == constants.Interests:
        getter = database.get_users_search_parameters_interests
        deleter = database.remove_from_users_search_parameters_interests
        appender = database.append_to_users_search_parameters_interests
        phrase = phrases.enter_interests
    else:
        getter = deleter = appender = phrase = None

    user_items = getter(call.message.chat.id)
    user_items = [] if user_items is None else user_items
    if item in user_items:
        deleter(call.message.chat.id, item)
    else:
        appender(call.message.chat.id, item)

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=phrase,
                          reply_markup=Keyboards.create_inline_keyboard_with_multiple_choice(
                              field,
                              getter(call.message.chat.id),
                              phrases.values_of_possible_answers))


# =====

def check_registration(user_id: int):
    if database.is_registered(user_id):
        activate_main_menu(user_id)
    else:  # Start registration procedure
        bot.send_message(user_id, text=phrases.we_ask_personal_data,
                         reply_markup=Keyboards.ask_personal_data)
        database.set_users_menu_id(user_id, constants.MenuIds.PERSONAL_DATA_MENU)


def check_search_parameters(user_id: int):
    if database.are_search_parameters_filled(user_id):
        activate_search_menu(user_id)
    else:  # Start filling search parameters procedure
        bot.send_message(user_id, text=phrases.user_have_not_search_parameters_yet)
        database.set_users_menu_id(user_id, constants.MenuIds.SEARCH_PARAMETERS_MENU)
        ask_search_parameters_age_groups(user_id)


def activate_main_menu(user_id: int):
    database.set_users_menu_id(user_id, constants.MenuIds.MAIN_MENU)
    bot.send_message(user_id, text=phrases.main_menu_title,
                     reply_markup=Keyboards.main_menu)


def activate_search_menu(user_id: int):
    database.set_users_menu_id(user_id, constants.MenuIds.SEARCH_MENU)
    bot.send_message(user_id, text=phrases.search_menu_title,
                     reply_markup=Keyboards.search_menu)


def activate_subscription_menu(user_id: int):
    database.set_users_menu_id(user_id, constants.MenuIds.SUBSCRIPTION_MENU)
    bot.send_message(user_id, text=phrases.about_subscription,
                     reply_markup=Keyboards.button_for_payment,
                     parse_mode="Markdown")

    bot.send_message(user_id, text=phrases.press_btn_after_purchase,
                     reply_markup=Keyboards.subscription_menu,
                     parse_mode="Markdown")


def activate_select_profile_item_to_edit_menu(user_id: int):
    show_users_profile(user_id)
    database.set_users_menu_id(user_id, constants.MenuIds.SELECT_PROFILE_ITEM_TO_EDIT_MENU)
    database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.NULL)
    bot.send_message(user_id,
                     text=phrases.edit_profile_menu,
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.send_message(user_id,
                     text=phrases.select_the_profile_item_to_edit,
                     reply_markup=Keyboards.create_inline_keyboard_from_list(
                         constants.ProfileItemsIds.get_all_not_null_ids(),
                         phrases.profile_items))


def activate_select_search_parameters_item_to_edit_menu(user_id: int):
    show_users_search_parameters(user_id)
    database.set_users_menu_id(user_id, constants.MenuIds.SELECT_SEARCH_PARAMETERS_ITEM_TO_EDIT_MENU)
    database.set_users_search_parameters_item_id(user_id, constants.SearchParametersItemsIds.NULL)

    bot.send_message(user_id,
                     text=phrases.edit_search_parameters_menu,
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.send_message(user_id,
                     text=phrases.select_the_search_parameters_item_to_edit,
                     reply_markup=Keyboards.create_inline_keyboard_from_list(
                         constants.SearchParametersItemsIds.get_all_not_null_ids(),
                         phrases.search_parameters_items))


def ask_profile_first_name(user_id: int):
    bot.send_message(user_id, text=phrases.enter_your_first_name,
                     reply_markup=Keyboards.profile_do_not_specify)
    database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.FIRST_NAME)


def ask_profile_last_name(user_id: int):
    database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.LAST_NAME)
    bot.send_message(user_id, text=phrases.enter_your_last_name)


def ask_profile_age(user_id: int):
    database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.AGE)
    bot.send_message(user_id, text=phrases.enter_your_age)


def ask_profile_spoken_languages(user_id: int):
    database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.SPOKEN_LANGUAGES)

    bot.send_message(user_id, text=phrases.enter_your_spoken_languages,
                     reply_markup=Keyboards.create_inline_keyboard_with_multiple_choice(
                         constants.SpokenLanguages,
                         database.get_users_profile_spoken_languages(user_id),
                         phrases.values_of_possible_answers))

    bot.send_message(user_id, text=phrases.after_choice,
                     reply_markup=Keyboards.profile_finish_and_skip)


def ask_profile_programming_languages(user_id: int):
    database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.PROGRAMMING_LANGUAGES)

    bot.send_message(user_id, text=phrases.enter_your_programming_languages,
                     reply_markup=Keyboards.create_inline_keyboard_with_multiple_choice(
                         constants.ProgrammingLanguages,
                         database.get_users_profile_programming_languages(user_id),
                         phrases.values_of_possible_answers))

    bot.send_message(user_id, text=phrases.after_choice,
                     reply_markup=Keyboards.profile_finish_and_skip)


def ask_profile_interests(user_id: int):
    database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.INTERESTS)

    bot.send_message(user_id, text=phrases.enter_your_interests,
                     reply_markup=Keyboards.create_inline_keyboard_with_multiple_choice(
                         constants.Interests,
                         database.get_users_profile_interests(user_id),
                         phrases.values_of_possible_answers))

    bot.send_message(user_id, text=phrases.after_choice,
                     reply_markup=Keyboards.profile_finish_and_skip)


def ask_search_parameters_age_groups(user_id: int):
    database.set_users_search_parameters_item_id(user_id, constants.SearchParametersItemsIds.AGE_GROUP)

    bot.send_message(user_id, text=phrases.enter_age_group_for_search,
                     reply_markup=Keyboards.create_inline_keyboard_with_multiple_choice(
                         constants.AgeGroups,
                         database.get_users_search_parameters_age_groups(user_id),
                         phrases.values_of_possible_answers))

    bot.send_message(user_id, text=phrases.after_choice,
                     reply_markup=Keyboards.search_parameters_finish_and_skip)


def ask_search_parameters_spoken_languages(user_id: int):
    database.set_users_search_parameters_item_id(user_id, constants.SearchParametersItemsIds.SPOKEN_LANGUAGES)

    bot.send_message(user_id, text=phrases.enter_spoken_languages,
                     reply_markup=Keyboards.create_inline_keyboard_with_multiple_choice(
                         constants.SpokenLanguages,
                         database.get_users_search_parameters_spoken_languages(user_id),
                         phrases.values_of_possible_answers))

    bot.send_message(user_id, text=phrases.after_choice,
                     reply_markup=Keyboards.search_parameters_finish_and_skip)


def ask_search_parameters_programming_languages(user_id: int):
    database.set_users_search_parameters_item_id(user_id, constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES)

    bot.send_message(user_id, text=phrases.enter_programming_languages,
                     reply_markup=Keyboards.create_inline_keyboard_with_multiple_choice(
                         constants.ProgrammingLanguages,
                         database.get_users_search_parameters_programming_languages(user_id),
                         phrases.values_of_possible_answers))

    bot.send_message(user_id, text=phrases.after_choice,
                     reply_markup=Keyboards.search_parameters_finish_and_skip)


def ask_search_parameters_interests(user_id: int):
    database.set_users_search_parameters_item_id(user_id, constants.SearchParametersItemsIds.INTERESTS)

    bot.send_message(user_id, text=phrases.enter_interests,
                     reply_markup=Keyboards.create_inline_keyboard_with_multiple_choice(
                         constants.Interests,
                         database.get_users_search_parameters_interests(user_id),
                         phrases.values_of_possible_answers))

    bot.send_message(user_id, text=phrases.after_choice,
                     reply_markup=Keyboards.search_parameters_finish_and_skip)


def show_users_profile(user_id: int):
    """
    Send a message to the user with his profile
    """
    database.set_users_menu_id(user_id, constants.MenuIds.CHECK_PROFILE_MENU)
    bot.send_message(user_id, text=phrases.your_profile)
    bot.send_message(user_id, text=User(user_id).get_profile(),
                     parse_mode="Markdown",
                     reply_markup=Keyboards.profile_ok_edit)


def show_users_search_parameters(user_id: int):
    """
    Send a message to the user with his search_parameters
    """
    database.set_users_menu_id(user_id, constants.MenuIds.CHECK_SEARCH_PARAMETERS_MENU)
    bot.send_message(user_id, text=phrases.your_search_parameters)
    bot.send_message(user_id, text=User(user_id).get_search_parameters(),
                     parse_mode="Markdown",
                     reply_markup=Keyboards.search_parameters_ok_edit)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_menu(constants.MenuIds.MAIN_MENU))
def processing_main_menu_items(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == constants.MainMenuItems.FIND_PEOPLE.get_str_value(phrases.values_of_main_menu_items):
        check_search_parameters(user_id)
    elif users_message == constants.MainMenuItems.SUBSCRIPTION.get_str_value(phrases.values_of_main_menu_items):
        activate_subscription_menu(user_id)
    elif users_message == constants.MainMenuItems.FIND_PROJECT.get_str_value(phrases.values_of_main_menu_items):
        bot.send_message(user_id, text=phrases.not_ready_yet)
    elif users_message == constants.MainMenuItems.FIND_PEOPLE_TO_THE_PROJECT.get_str_value(
            phrases.values_of_main_menu_items):
        bot.send_message(user_id, text=phrases.not_ready_yet)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_menu(
                         constants.MenuIds.CHECK_PROFILE_MENU))
def processing_check_profile_items_menu(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.ok_edit[0]:
        activate_main_menu(user_id)
    elif users_message == phrases.ok_edit[1]:
        activate_select_profile_item_to_edit_menu(user_id)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_menu(
                         constants.MenuIds.CHECK_SEARCH_PARAMETERS_MENU))
def processing_check_search_parameters_items_menu(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.ok_edit[0]:
        activate_search_menu(user_id)
    elif users_message == phrases.ok_edit[1]:
        activate_select_search_parameters_item_to_edit_menu(user_id)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_registration_item(
                         constants.ProfileItemsIds.FIRST_NAME))
def processing_registration_item_first_name(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.do_not_specify:
        database.set_users_profile_first_name(user_id, value=None)
    else:
        database.set_users_profile_first_name(user_id, value=users_message)

    if database.get_users_menu_id(user_id) == constants.MenuIds.REGISTRATION_MENU:
        ask_profile_last_name(user_id)
    elif database.get_users_menu_id(user_id) == constants.MenuIds.EDIT_PROFILE_MENU:
        show_users_profile(user_id)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_registration_item(
                         constants.ProfileItemsIds.LAST_NAME))
def processing_registration_item_last_name(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.do_not_specify:
        database.set_users_profile_last_name(user_id, value=None)
    else:
        database.set_users_profile_last_name(user_id, value=users_message)

    if database.get_users_menu_id(user_id) == constants.MenuIds.REGISTRATION_MENU:
        ask_profile_age(user_id)
    elif database.get_users_menu_id(user_id) == constants.MenuIds.EDIT_PROFILE_MENU:
        show_users_profile(user_id)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_registration_item(
                         constants.ProfileItemsIds.AGE))
def processing_registration_item_age(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.do_not_specify:
        database.set_users_profile_age(user_id, value=None)
    elif users_message.isdigit():
        database.set_users_profile_age(user_id, value=users_message)
    else:
        bot.send_message(user_id, text=phrases.enter_correct_age)

    if users_message == phrases.do_not_specify or users_message.isdigit():
        if database.get_users_menu_id(user_id) == constants.MenuIds.REGISTRATION_MENU:
            ask_profile_spoken_languages(user_id)
        elif database.get_users_menu_id(user_id) == constants.MenuIds.EDIT_PROFILE_MENU:
            show_users_profile(user_id)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_registration_item(
                         constants.ProfileItemsIds.SPOKEN_LANGUAGES))
def processing_registration_item_spoken_language(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.do_not_specify:
        database.set_users_profile_spoken_languages_null(user_id)

    if users_message in (phrases.do_not_specify, phrases.finish_typing):
        if database.get_users_menu_id(user_id) == constants.MenuIds.REGISTRATION_MENU:
            ask_profile_programming_languages(user_id)
        elif database.get_users_menu_id(user_id) == constants.MenuIds.EDIT_PROFILE_MENU:
            show_users_profile(user_id)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_registration_item(
                         constants.ProfileItemsIds.PROGRAMMING_LANGUAGES))
def processing_registration_item_programming_language(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.do_not_specify:
        database.set_users_profile_programming_languages_null(user_id)

    if users_message in (phrases.do_not_specify, phrases.finish_typing):
        if database.get_users_menu_id(user_id) == constants.MenuIds.REGISTRATION_MENU:
            ask_profile_interests(user_id)
        elif database.get_users_menu_id(user_id) == constants.MenuIds.EDIT_PROFILE_MENU:
            show_users_profile(user_id)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_registration_item(
                         constants.ProfileItemsIds.INTERESTS))
def processing_registration_item_interests(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.do_not_specify:
        database.set_users_profile_interests_null(user_id)

    if users_message in (phrases.do_not_specify, phrases.finish_typing):
        if database.get_users_menu_id(user_id) == constants.MenuIds.REGISTRATION_MENU:
            database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.NULL)
            database.register_user(user_id)
            bot.send_message(user_id, text=phrases.finish_registration,
                             reply_markup=telebot.types.ReplyKeyboardRemove())
            show_users_profile(user_id)
        elif database.get_users_menu_id(user_id) == constants.MenuIds.EDIT_PROFILE_MENU:
            show_users_profile(user_id)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_search_parameters_item(
                         constants.SearchParametersItemsIds.AGE_GROUP))
def processing_search_parameter_item_age_group(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.does_not_matter:
        database.set_users_profile_search_parameters_age_groups_null(user_id)

    if users_message in (phrases.does_not_matter, phrases.finish_typing):

        if database.get_users_menu_id(user_id) == constants.MenuIds.SEARCH_PARAMETERS_MENU:
            ask_search_parameters_spoken_languages(user_id)
        elif database.get_users_menu_id(user_id) == constants.MenuIds.EDIT_SEARCH_PARAMETERS_MENU:
            show_users_search_parameters(user_id)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_search_parameters_item(
                         constants.SearchParametersItemsIds.SPOKEN_LANGUAGES))
def processing_search_parameter_item_spoken_languages(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.does_not_matter:
        database.set_users_profile_search_parameters_spoken_languages_null(user_id)

    if users_message in (phrases.does_not_matter, phrases.finish_typing):
        if database.get_users_menu_id(user_id) == constants.MenuIds.SEARCH_PARAMETERS_MENU:
            ask_search_parameters_programming_languages(user_id)
        elif database.get_users_menu_id(user_id) == constants.MenuIds.EDIT_SEARCH_PARAMETERS_MENU:
            show_users_search_parameters(user_id)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_search_parameters_item(
                         constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES))
def processing_search_parameter_item_programming_languages(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.does_not_matter:
        database.set_users_profile_search_parameters_programming_languages_null(user_id)

    if users_message in (phrases.does_not_matter, phrases.finish_typing):
        if database.get_users_menu_id(user_id) == constants.MenuIds.SEARCH_PARAMETERS_MENU:
            ask_search_parameters_interests(user_id)
        elif database.get_users_menu_id(user_id) == constants.MenuIds.EDIT_SEARCH_PARAMETERS_MENU:
            show_users_search_parameters(user_id)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_search_parameters_item(
                         constants.SearchParametersItemsIds.INTERESTS))
def processing_search_parameter_item_interests(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.does_not_matter:
        database.set_users_profile_search_parameters_interests_null(user_id)

    if users_message in (phrases.does_not_matter, phrases.finish_typing):
        if database.get_users_menu_id(user_id) == constants.MenuIds.SEARCH_PARAMETERS_MENU:
            database.set_users_search_parameters_item_id(user_id,
                                                         constants.SearchParametersItemsIds.NULL)
            database.set_search_parameters_filled(user_id)
            bot.send_message(user_id, text=phrases.finish_enter_search_parameters,
                             reply_markup=telebot.types.ReplyKeyboardRemove())
            show_users_search_parameters(user_id)
        elif database.get_users_menu_id(user_id) == constants.MenuIds.EDIT_SEARCH_PARAMETERS_MENU:
            show_users_search_parameters(user_id)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_menu(constants.MenuIds.SEARCH_MENU))
def processing_search_menu_items(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == constants.SearchMenuItems.FIND.get_str_value(phrases.values_of_search_menu_items):
        database.set_users_menu_id(user_id, constants.MenuIds.PROFILE_REACTIONS_MENU)
        bot.send_message(user_id, text=phrases.candidates_profiles,
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        User(message.chat.id).create_candidates_list()
        show_candidates_profile(user_id)
    elif users_message == constants.SearchMenuItems.EDIT_SEARCH_PARAMETERS.get_str_value(
            phrases.values_of_search_menu_items):
        activate_select_search_parameters_item_to_edit_menu(user_id)
    elif users_message == constants.SearchMenuItems.EDIT_PROFILE.get_str_value(phrases.values_of_search_menu_items):
        activate_select_profile_item_to_edit_menu(user_id)
    elif users_message == constants.SearchMenuItems.GO_TO_MAIN_MENU.get_str_value(phrases.values_of_search_menu_items):
        activate_main_menu(user_id)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_menu(constants.MenuIds.SUBSCRIPTION_MENU))
def processing_subscription_menu_items(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.paid:
        bot.send_message(user_id, text=phrases.after_purchase)
        database.activate_subscription(user_id)
        activate_main_menu(user_id)


def show_candidates_profile(user_id: int):
    candidate_id = User(user_id).get_candidate_id()
    if candidate_id is None:
        bot.send_message(user_id, text=phrases.no_profiles_more,
                         parse_mode="Markdown",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        activate_main_menu(user_id)
    else:
        bot.send_message(user_id, text=User(candidate_id).get_profile(),
                         parse_mode="Markdown",
                         reply_markup=Keyboards.profile_reaction_menu)
        database.set_users_last_shown_profile_id(user_id, candidate_id)
        database.mark_profile_as_viewed(user_id, candidate_id)
