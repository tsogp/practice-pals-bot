import telebot
import phrases_ru as phrases
import constants
import search
from keyboards import Keyboards

import bottoken
from database import Database

bot = telebot.TeleBot(bottoken.TOKEN)  # Main bot object
database = Database()


def run():
    bot.polling(none_stop=True)


@bot.message_handler(commands=['start'])
def __start(message):
    """
    Processing the command "/start"
    """
    bot.send_message(message.chat.id,
                     text=phrases.welcome_message,
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    __check_registration(message.chat.id)


@bot.message_handler(commands=['main_menu'])
def __main_menu(message):
    """
    Processing the command "/main_menu"
    """
    __activate_main_menu(message.chat.id)


@bot.message_handler(content_types=["text"])
def __processing_all_text_messages(message):
    users_message = message.text
    users_menu_id = database.get_users_menu_id(message.chat.id)
    if users_menu_id == constants.MenuIds.REGISTRATION_MENU:
        __processing_registration_menu_items(users_message, message.chat.id, message.from_user.username)
    elif users_menu_id == constants.MenuIds.CHECK_PROFILE_MENU:
        __processing_check_profile_items_menu(users_message, message.chat.id)
    elif users_menu_id == constants.MenuIds.MAIN_MENU:
        __processing_main_menu_items(users_message, message.chat.id)
    elif users_menu_id == constants.MenuIds.SEARCH_PARAMETERS_MENU:
        __processing_search_parameters_menu_items(users_message, message.chat.id)
    elif users_menu_id == constants.MenuIds.CHECK_SEARCH_PARAMETERS_MENU:
        __processing_check_search_parameters_items_menu(users_message, message.chat.id)
    elif users_menu_id == constants.MenuIds.SEARCH_MENU:
        __processing_search_menu_items(users_message, message.chat.id)
    else:
        bot.send_message(message.chat.id, text=phrases.call_main_menu)


def __is_like_acceptable(user_id: int):
    return database.get_remaining_number_of_likes(user_id) > 0


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    """Inline-keyboards button's click handler"""
    users_active_menu_id = database.get_users_menu_id(call.message.chat.id)
    bot.answer_callback_query(callback_query_id=call.id, text='')
    if users_active_menu_id == constants.MenuIds.PROFILE_REACTIONS_MENU:
        if call.data == constants.PROFILE_REACTIONS_MENU_PREFIX + "0":
            candidate_id = database.get_users_shown_profile_id(call.message.chat.id)
            if candidate_id is None:
                return
            if __is_like_acceptable(call.message.chat.id):
                candidate_login = database.get_users_telegram_login_by_id(candidate_id)
                bot.send_message(call.message.chat.id, text=phrases.telegram_login + candidate_login)
                database.dec_remaining_number_of_likes(call.message.chat.id)
            else:
                bot.send_message(call.message.chat.id, text=phrases.likes_blocked)
            database.set_users_shown_profile_id(call.message.chat.id, None)

        elif call.data == constants.PROFILE_REACTIONS_MENU_PREFIX + "1":
            __show_candidates_profile(call.message.chat.id)
        elif call.data == constants.PROFILE_REACTIONS_MENU_PREFIX + "2":
            __activate_main_menu(call.message.chat.id)


def __check_registration(user_id: int):
    if database.is_registered(user_id):
        __activate_main_menu(user_id)
    else:  # Start registration procedure
        bot.send_message(user_id, text=phrases.user_not_registered_yet)
        bot.send_message(user_id, text=phrases.enter_your_first_name,
                         reply_markup=Keyboards.profile_do_not_specify)
        database.set_users_menu_id(user_id, constants.MenuIds.REGISTRATION_MENU)
        database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.FIRST_NAME)


def __check_search_parameters(user_id: int):
    if database.are_search_parameters_filled(user_id):
        __activate_search_menu(user_id)
    else:  # Start filling search parameters procedure
        bot.send_message(user_id, text=phrases.user_have_not_search_parameters_yet)
        bot.send_message(user_id, text=phrases.enter_age_group_for_search,
                         reply_markup=Keyboards.search_parameters_age_groups)
        database.set_users_menu_id(user_id, constants.MenuIds.SEARCH_PARAMETERS_MENU)
        database.set_users_search_parameter_item_id(user_id, constants.SearchParametersItemsIds.AGE_GROUP)


def __activate_main_menu(user_id: int):
    database.set_users_menu_id(user_id, constants.MenuIds.MAIN_MENU)
    bot.send_message(user_id, text=phrases.main_menu_title,
                     reply_markup=Keyboards.main_menu)


def __activate_search_menu(user_id: int):
    database.set_users_menu_id(user_id, constants.MenuIds.SEARCH_MENU)
    bot.send_message(user_id, text=phrases.search_menu_title,
                     reply_markup=Keyboards.search_menu)


def __show_users_profile(user_id: int):
    """
    Send a message to the user with his profile
    """
    database.set_users_menu_id(user_id, constants.MenuIds.CHECK_PROFILE_MENU)
    bot.send_message(user_id, text=phrases.your_profile)
    bot.send_message(user_id, text=__generate_string_with_users_profile(user_id),
                     parse_mode="Markdown",
                     reply_markup=Keyboards.profile_ok_edit)


def __generate_string_with_users_profile(user_id: int):
    profile_str = ""
    profile_items_ids = [member for member in constants.ProfileItemsIds if member.name != "NULL"]
    for profile_item_id in profile_items_ids:
        profile_str += (f"*{phrases.profile_items[profile_item_id]}:* " +
                        database.get_users_profile_item(user_id, profile_item_id) + "\n")
    return profile_str


def __show_users_search_parameters(user_id: int):
    """
    Send a message to the user with his search_parameters
    """
    database.set_users_menu_id(user_id, constants.MenuIds.CHECK_SEARCH_PARAMETERS_MENU)
    bot.send_message(user_id, text=phrases.your_search_parameters)
    bot.send_message(user_id, text=__generate_string_with_users_search_parameters(user_id),
                     parse_mode="Markdown",
                     reply_markup=Keyboards.search_parameters_ok_edit)


def __generate_string_with_users_search_parameters(user_id: int):
    search_parameters_str = ""
    search_parameters_items_ids = [member for member in constants.SearchParametersItemsIds if
                                   member.name != "NULL"]
    for search_parameters_item_id in search_parameters_items_ids:
        search_parameters_str += (f"*{phrases.search_parameters_items[search_parameters_item_id]}:* " +
                                  database.get_users_search_parameter_item(user_id,
                                                                           search_parameters_item_id) + "\n")
    return search_parameters_str


def __processing_main_menu_items(users_message: str, user_id: int):
    if users_message == phrases.main_menu_list[0]:
        __check_search_parameters(user_id)
    elif users_message == phrases.main_menu_list[1]:
        bot.send_message(user_id, text=phrases.not_ready_yet)
    elif users_message == phrases.main_menu_list[2]:
        bot.send_message(user_id, text=phrases.not_ready_yet)


def __processing_check_profile_items_menu(users_message: str, user_id: int):
    if users_message == phrases.ok_edit[0]:
        __activate_main_menu(user_id)
    elif users_message == phrases.ok_edit[1]:
        bot.send_message(user_id, text=phrases.not_ready_yet)
        __activate_main_menu(user_id)


def __processing_check_search_parameters_items_menu(users_message: str, user_id: int):
    if users_message == phrases.ok_edit[0]:
        __activate_search_menu(user_id)
    elif users_message == phrases.ok_edit[1]:
        bot.send_message(user_id, text=phrases.not_ready_yet)
        __activate_search_menu(user_id)


def __processing_registration_menu_items(users_message: str, user_id: int, user_name: str):
    users_registration_item_id = database.get_users_registration_item_id(user_id)
    if users_registration_item_id == constants.ProfileItemsIds.FIRST_NAME:
        __processing_registration_item_first_name(users_message, user_id)
    elif users_registration_item_id == constants.ProfileItemsIds.LAST_NAME:
        __processing_registration_item_last_name(users_message, user_id)
    elif users_registration_item_id == constants.ProfileItemsIds.AGE:
        __processing_registration_item_age(users_message, user_id)
    elif users_registration_item_id == constants.ProfileItemsIds.SPOKEN_LANGUAGES:
        __processing_registration_item_spoken_language(users_message, user_id)
    elif users_registration_item_id == constants.ProfileItemsIds.PROGRAMMING_LANGUAGES:
        __processing_registration_item_programming_language(users_message, user_id)
    elif users_registration_item_id == constants.ProfileItemsIds.INTERESTS:
        __processing_registration_item_interests(users_message, user_id, user_name)


def __processing_registration_item_first_name(users_message: str, user_id: int):
    if users_message == phrases.do_not_specify:
        database.set_users_registration_item(user_id,
                                             item=constants.ProfileItemsIds.FIRST_NAME,
                                             value=None)
    else:
        database.set_users_registration_item(user_id,
                                             item=constants.ProfileItemsIds.FIRST_NAME,
                                             value=users_message)

    database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.LAST_NAME)
    bot.send_message(user_id, text=phrases.enter_your_last_name)


def __processing_registration_item_last_name(users_message: str, user_id: int):
    if users_message == phrases.do_not_specify:
        database.set_users_registration_item(user_id,
                                             item=constants.ProfileItemsIds.LAST_NAME,
                                             value=None)
    else:
        database.set_users_registration_item(user_id,
                                             item=constants.ProfileItemsIds.LAST_NAME,
                                             value=users_message)

    database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.AGE)
    bot.send_message(user_id, text=phrases.enter_your_age)


def __processing_registration_item_age(users_message: str, user_id: int):
    if users_message == phrases.do_not_specify:
        database.set_users_registration_item(user_id, item=constants.ProfileItemsIds.AGE, value=None)
    elif users_message.isdigit():
        database.set_users_registration_item(user_id,
                                             item=constants.ProfileItemsIds.AGE,
                                             value=users_message)
    else:
        bot.send_message(user_id, text=phrases.enter_correct_age)

    if users_message == phrases.do_not_specify or users_message.isdigit():
        database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.SPOKEN_LANGUAGES)
        bot.send_message(user_id, text=phrases.enter_your_spoken_languages,
                         reply_markup=Keyboards.profile_spoken_languages)


def __processing_registration_item_spoken_language(users_message: str, user_id: int):
    if users_message == phrases.do_not_specify:
        database.set_users_registration_item(user_id,
                                             item=constants.ProfileItemsIds.SPOKEN_LANGUAGES,
                                             value=None)
    elif users_message in phrases.spoken_languages:
        database.append_to_users_registration_item(user_id,
                                                   item=constants.ProfileItemsIds.SPOKEN_LANGUAGES,
                                                   value=users_message)
    elif users_message != phrases.finish_typing:
        bot.send_message(user_id, text=phrases.select_from_the_list)

    if users_message in (phrases.do_not_specify, phrases.finish_typing):
        database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.PROGRAMMING_LANGUAGES)
        bot.send_message(user_id, text=phrases.enter_your_programming_languages,
                         reply_markup=Keyboards.profile_programming_languages)


def __processing_registration_item_programming_language(users_message: str, user_id: int):
    if users_message == phrases.do_not_specify:
        database.set_users_registration_item(user_id,
                                             item=constants.ProfileItemsIds.PROGRAMMING_LANGUAGES, value=None)
    elif users_message in phrases.programming_languages:
        database.append_to_users_registration_item(user_id,
                                                   item=constants.ProfileItemsIds.PROGRAMMING_LANGUAGES,
                                                   value=users_message)
    elif users_message != phrases.finish_typing:
        bot.send_message(user_id, text=phrases.select_from_the_list)

    if users_message in (phrases.do_not_specify, phrases.finish_typing):
        database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.INTERESTS)
        bot.send_message(user_id, text=phrases.enter_your_interests,
                         reply_markup=Keyboards.profile_interests)


def __processing_registration_item_interests(users_message: str, user_id: int, user_name: str):
    if users_message == phrases.do_not_specify:
        database.set_users_registration_item(user_id,
                                             item=constants.ProfileItemsIds.INTERESTS, value=None)
    elif users_message in phrases.interests:
        database.append_to_users_registration_item(user_id,
                                                   item=constants.ProfileItemsIds.INTERESTS,
                                                   value=users_message)
    elif users_message != phrases.finish_typing:
        bot.send_message(user_id, text=phrases.select_from_the_list)

    if users_message in (phrases.do_not_specify, phrases.finish_typing):
        database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.NULL)
        database.register_user(user_id, user_name)
        bot.send_message(user_id, text=phrases.finish_registration,
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        __show_users_profile(user_id)


def __processing_search_parameters_menu_items(users_message: str, user_id: int):
    users_search_parameter_item_id = database.get_users_search_parameter_item_id(user_id)
    if users_search_parameter_item_id == constants.SearchParametersItemsIds.AGE_GROUP:
        __processing_search_parameter_item_age_group(users_message, user_id)
    elif users_search_parameter_item_id == constants.SearchParametersItemsIds.SPOKEN_LANGUAGES:
        __processing_search_parameter_item_spoken_languages(users_message, user_id)
    elif users_search_parameter_item_id == constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES:
        __processing_search_parameter_item_programming_languages(users_message, user_id)
    elif users_search_parameter_item_id == constants.SearchParametersItemsIds.INTERESTS:
        __processing_search_parameter_item_interests(users_message, user_id)


def __processing_search_parameter_item_age_group(users_message: str, user_id: int):
    if users_message == phrases.does_not_matter:
        database.append_to_users_search_parameter_item(user_id,
                                                       item=constants.SearchParametersItemsIds.AGE_GROUP,
                                                       value=None)
    elif users_message in phrases.age_groups:
        database.append_to_users_search_parameter_item(user_id,
                                                       item=constants.SearchParametersItemsIds.AGE_GROUP,
                                                       value=users_message)
    elif users_message != phrases.finish_typing:
        bot.send_message(user_id, text=phrases.select_from_the_list)

    if users_message in (phrases.does_not_matter, phrases.finish_typing):
        database.set_users_search_parameter_item_id(user_id,
                                                    constants.SearchParametersItemsIds.SPOKEN_LANGUAGES)
        bot.send_message(user_id, text=phrases.enter_spoken_languages,
                         reply_markup=Keyboards.search_parameters_spoken_languages)


def __processing_search_parameter_item_spoken_languages(users_message: str, user_id: int):
    if users_message == phrases.does_not_matter:
        database.append_to_users_search_parameter_item(user_id,
                                                       item=constants.SearchParametersItemsIds.SPOKEN_LANGUAGES,
                                                       value=None)
    elif users_message in phrases.spoken_languages:
        database.append_to_users_search_parameter_item(user_id,
                                                       item=constants.SearchParametersItemsIds.SPOKEN_LANGUAGES,
                                                       value=users_message)
    elif users_message != phrases.finish_typing:
        bot.send_message(user_id, text=phrases.select_from_the_list)

    if users_message in (phrases.does_not_matter, phrases.finish_typing):
        database.set_users_search_parameter_item_id(user_id,
                                                    constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES)
        bot.send_message(user_id, text=phrases.enter_programming_languages,
                         reply_markup=Keyboards.search_parameters_programming_languages)


def __processing_search_parameter_item_programming_languages(users_message: str, user_id: int):
    if users_message == phrases.does_not_matter:
        database.append_to_users_search_parameter_item(user_id,
                                                       item=constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES,
                                                       value=None)
    elif users_message in phrases.programming_languages:
        database.append_to_users_search_parameter_item(user_id,
                                                       item=constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES,
                                                       value=users_message)
    elif users_message != phrases.finish_typing:
        bot.send_message(user_id, text=phrases.select_from_the_list)

    if users_message in (phrases.does_not_matter, phrases.finish_typing):
        database.set_users_search_parameter_item_id(user_id,
                                                    constants.SearchParametersItemsIds.INTERESTS)
        bot.send_message(user_id, text=phrases.enter_interests,
                         reply_markup=Keyboards.search_parameters_interests)


def __processing_search_parameter_item_interests(users_message: str, user_id: int):
    if users_message == phrases.does_not_matter:
        database.append_to_users_search_parameter_item(user_id,
                                                       item=constants.SearchParametersItemsIds.INTERESTS,
                                                       value=None)
    elif users_message in phrases.interests:
        database.append_to_users_search_parameter_item(user_id,
                                                       item=constants.SearchParametersItemsIds.INTERESTS,
                                                       value=users_message)
    elif users_message != phrases.finish_typing:
        bot.send_message(user_id, text=phrases.select_from_the_list)

    if users_message in (phrases.does_not_matter, phrases.finish_typing):
        database.set_users_search_parameter_item_id(user_id,
                                                    constants.SearchParametersItemsIds.NULL)
        database.set_search_parameters_filled(user_id)
        bot.send_message(user_id, text=phrases.finish_enter_search_parameters,
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        __show_users_search_parameters(user_id)


def __processing_search_menu_items(users_message: str, user_id: int):
    if users_message == phrases.search_menu_list[0]:
        database.set_users_menu_id(user_id, constants.MenuIds.PROFILE_REACTIONS_MENU)
        bot.send_message(user_id, text=phrases.candidates_profiles,
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        __show_candidates_profile(user_id)
    elif users_message == phrases.search_menu_list[1]:
        bot.send_message(user_id, text=phrases.not_ready_yet)
    elif users_message == phrases.search_menu_list[2]:
        bot.send_message(user_id, text=phrases.not_ready_yet)


def __show_candidates_profile(user_id: int):
    candidate_id = search.Search.get_candidate_id(user_id)
    bot.send_message(user_id, text=__generate_string_with_users_profile(candidate_id),
                     parse_mode="Markdown",
                     reply_markup=Keyboards.profile_reaction_menu)
    database.set_users_shown_profile_id(user_id, candidate_id)
