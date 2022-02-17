import telebot

import phrases_ru as phrases
import constants
from keyboards import Keyboards
import bottoken

from IDatabase import IDatabase
from RealDatabase import Database

from User import User

bot = telebot.TeleBot(bottoken.TOKEN)  # Telegram bot object
database: IDatabase = Database()
User.set_database(database)


def run_bot() -> None:
    """
    Call to run bot
    """
    bot.polling(none_stop=True)


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
    activate_main_menu(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    """Inline-keyboards button's click handler"""
    users_active_menu_id = database.get_users_menu_id(call.message.chat.id)
    bot.answer_callback_query(callback_query_id=call.id, text='')
    if users_active_menu_id == constants.MenuIds.PROFILE_REACTIONS_MENU:
        if call.data == constants.PROFILE_REACTIONS_MENU_PREFIX + "0":
            processing_like_button(call.message.chat.id)
        elif call.data == constants.PROFILE_REACTIONS_MENU_PREFIX + "1":
            show_candidates_profile(call.message.chat.id)
        elif call.data == constants.PROFILE_REACTIONS_MENU_PREFIX + "2":
            activate_main_menu(call.message.chat.id)
        elif call.data == constants.GO_TO_SUBSCRIPTION_MENU_PREFIX + "0":
            activate_subscription_menu(call.message.chat.id)


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


def check_registration(user_id: int):
    if database.is_registered(user_id):
        activate_main_menu(user_id)
    else:  # Start registration procedure
        bot.send_message(user_id, text=phrases.user_not_registered_yet)
        bot.send_message(user_id, text=phrases.enter_your_first_name,
                         reply_markup=Keyboards.profile_do_not_specify)
        database.set_users_menu_id(user_id, constants.MenuIds.REGISTRATION_MENU)
        database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.FIRST_NAME)


def check_search_parameters(user_id: int):
    if database.are_search_parameters_filled(user_id):
        activate_search_menu(user_id)
    else:  # Start filling search parameters procedure
        bot.send_message(user_id, text=phrases.user_have_not_search_parameters_yet)
        bot.send_message(user_id, text=phrases.enter_age_group_for_search,
                         reply_markup=Keyboards.search_parameters_age_groups)
        database.set_users_menu_id(user_id, constants.MenuIds.SEARCH_PARAMETERS_MENU)
        database.set_users_search_parameters_item_id(user_id, constants.SearchParametersItemsIds.AGE_GROUP)


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
        bot.send_message(user_id, text=phrases.not_ready_yet)
        activate_main_menu(user_id)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_menu(
                         constants.MenuIds.CHECK_SEARCH_PARAMETERS_MENU))
def processing_check_search_parameters_items_menu(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.ok_edit[0]:
        activate_search_menu(user_id)
    elif users_message == phrases.ok_edit[1]:
        bot.send_message(user_id, text=phrases.not_ready_yet)
        activate_search_menu(user_id)


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

    database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.LAST_NAME)
    bot.send_message(user_id, text=phrases.enter_your_last_name)


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

    database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.AGE)
    bot.send_message(user_id, text=phrases.enter_your_age)


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
        database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.SPOKEN_LANGUAGES)
        bot.send_message(user_id, text=phrases.enter_your_spoken_languages,
                         reply_markup=Keyboards.profile_spoken_languages)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_registration_item(
                         constants.ProfileItemsIds.SPOKEN_LANGUAGES))
def processing_registration_item_spoken_language(message):
    users_message = message.text
    user_id = message.chat.id
    if users_message == phrases.do_not_specify:
        database.set_users_profile_spoken_languages_null(user_id)
    elif users_message in constants.SpokenLanguages.get_all_str_vales(phrases.values_of_enums_constants):
        database.append_to_users_profile_spoken_languages(user_id,
                                                          value=constants.SpokenLanguages.get_object_by_str_value(
                                                              users_message,
                                                              phrases.values_of_enums_constants))
    elif users_message != phrases.finish_typing:
        bot.send_message(user_id, text=phrases.select_from_the_list)

    if users_message in (phrases.do_not_specify, phrases.finish_typing):
        database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.PROGRAMMING_LANGUAGES)
        bot.send_message(user_id, text=phrases.enter_your_programming_languages,
                         reply_markup=Keyboards.profile_programming_languages)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_registration_item(
                         constants.ProfileItemsIds.PROGRAMMING_LANGUAGES))
def processing_registration_item_programming_language(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.do_not_specify:
        database.set_users_profile_programming_languages_null(user_id)
    elif users_message in constants.ProgrammingLanguages.get_all_str_vales(phrases.values_of_enums_constants):
        database.append_to_users_profile_programming_languages(
            user_id,
            value=constants.ProgrammingLanguages.get_object_by_str_value(users_message,
                                                                         phrases.values_of_enums_constants))
    elif users_message != phrases.finish_typing:
        bot.send_message(user_id, text=phrases.select_from_the_list)

    if users_message in (phrases.do_not_specify, phrases.finish_typing):
        database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.INTERESTS)
        bot.send_message(user_id, text=phrases.enter_your_interests,
                         reply_markup=Keyboards.profile_interests)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_registration_item(
                         constants.ProfileItemsIds.INTERESTS))
def processing_registration_item_interests(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.do_not_specify:
        database.set_users_profile_interests_null(user_id)
    elif users_message in constants.Interests.get_all_str_vales(phrases.values_of_enums_constants):
        database.append_to_users_profile_interests(user_id, value=constants.Interests.get_object_by_str_value(
            users_message,
            phrases.values_of_enums_constants))
    elif users_message != phrases.finish_typing:
        bot.send_message(user_id, text=phrases.select_from_the_list)

    if users_message in (phrases.do_not_specify, phrases.finish_typing):
        database.set_users_registration_item_id(user_id, constants.ProfileItemsIds.NULL)
        database.register_user(user_id)
        bot.send_message(user_id, text=phrases.finish_registration,
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        show_users_profile(user_id)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_search_parameters_item(
                         constants.SearchParametersItemsIds.AGE_GROUP))
def processing_search_parameter_item_age_group(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.does_not_matter:
        database.set_users_profile_search_parameters_age_groups_null(user_id)
    elif users_message in constants.AgeGroups.get_all_str_vales(phrases.values_of_enums_constants):
        database.append_to_users_search_parameters_age_groups(user_id,
                                                              value=constants.AgeGroups.get_object_by_str_value(
                                                                  users_message,
                                                                  phrases.values_of_enums_constants))
    elif users_message != phrases.finish_typing:
        bot.send_message(user_id, text=phrases.select_from_the_list)

    if users_message in (phrases.does_not_matter, phrases.finish_typing):
        database.set_users_search_parameters_item_id(user_id,
                                                     constants.SearchParametersItemsIds.SPOKEN_LANGUAGES)
        bot.send_message(user_id, text=phrases.enter_spoken_languages,
                         reply_markup=Keyboards.search_parameters_spoken_languages)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_search_parameters_item(
                         constants.SearchParametersItemsIds.SPOKEN_LANGUAGES))
def processing_search_parameter_item_spoken_languages(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.does_not_matter:
        database.set_users_profile_search_parameters_spoken_languages_null(user_id)
    elif users_message in constants.SpokenLanguages.get_all_str_vales(phrases.values_of_enums_constants):
        database.append_to_users_search_parameters_spoken_languages(
            user_id,
            value=constants.SpokenLanguages.get_object_by_str_value(users_message,
                                                                    phrases.values_of_enums_constants))
    elif users_message != phrases.finish_typing:
        bot.send_message(user_id, text=phrases.select_from_the_list)

    if users_message in (phrases.does_not_matter, phrases.finish_typing):
        database.set_users_search_parameters_item_id(user_id,
                                                     constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES)
        bot.send_message(user_id, text=phrases.enter_programming_languages,
                         reply_markup=Keyboards.search_parameters_programming_languages)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_search_parameters_item(
                         constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES))
def processing_search_parameter_item_programming_languages(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.does_not_matter:
        database.set_users_profile_search_parameters_programming_languages_null(user_id)
    elif users_message in constants.ProgrammingLanguages.get_all_str_vales(phrases.values_of_enums_constants):
        database.append_to_users_search_parameters_programming_languages(
            user_id,
            value=constants.ProgrammingLanguages.get_object_by_str_value(users_message,
                                                                         phrases.values_of_enums_constants))
    elif users_message != phrases.finish_typing:
        bot.send_message(user_id, text=phrases.select_from_the_list)

    if users_message in (phrases.does_not_matter, phrases.finish_typing):
        database.set_users_search_parameters_item_id(user_id,
                                                     constants.SearchParametersItemsIds.INTERESTS)
        bot.send_message(user_id, text=phrases.enter_interests,
                         reply_markup=Keyboards.search_parameters_interests)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_search_parameters_item(
                         constants.SearchParametersItemsIds.INTERESTS))
def processing_search_parameter_item_interests(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.does_not_matter:
        database.set_users_profile_search_parameters_interests_null(user_id)
    elif users_message in constants.Interests.get_all_str_vales(phrases.values_of_enums_constants):
        database.append_to_users_search_parameters_interests(user_id, value=constants.Interests.get_object_by_str_value(
            users_message,
            phrases.values_of_enums_constants))
    elif users_message != phrases.finish_typing:
        bot.send_message(user_id, text=phrases.select_from_the_list)

    if users_message in (phrases.does_not_matter, phrases.finish_typing):
        database.set_users_search_parameters_item_id(user_id,
                                                     constants.SearchParametersItemsIds.NULL)
        database.set_search_parameters_filled(user_id)
        bot.send_message(user_id, text=phrases.finish_enter_search_parameters,
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        show_users_search_parameters(user_id)


@bot.message_handler(content_types=["text"],
                     func=lambda message: User(message.chat.id).is_in_menu(constants.MenuIds.SEARCH_MENU))
def processing_search_menu_items(message):
    users_message = message.text
    user_id = message.chat.id

    if users_message == phrases.search_menu_list[0]:
        database.set_users_menu_id(user_id, constants.MenuIds.PROFILE_REACTIONS_MENU)
        bot.send_message(user_id, text=phrases.candidates_profiles,
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        User(message.chat.id).create_candidates_list()
        show_candidates_profile(user_id)
    elif users_message == phrases.search_menu_list[1]:
        bot.send_message(user_id, text=phrases.not_ready_yet)
    elif users_message == phrases.search_menu_list[2]:
        bot.send_message(user_id, text=phrases.not_ready_yet)


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
