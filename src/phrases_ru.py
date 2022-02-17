# File with phrases for the interface in Russian
from typing import List
import enum

import constants

welcome_message = "\U0001F44B Привет! Я Practice Pals Bot.\nПомогу Вам найти друзей по интересам в IT-сфере"

main_menu_title = "\U0001F3E0 Вы находитесь в главном меню"

values_of_main_menu_items = {
    constants.MainMenuItems.FIND_PEOPLE: "\U0001F91D Найти единомышленников",
    constants.MainMenuItems.SUBSCRIPTION: "\U00002B50 Подписка",
    constants.MainMenuItems.FIND_PROJECT: "\U0001F5C2 Найти проект",
    constants.MainMenuItems.FIND_PEOPLE_TO_THE_PROJECT: "\U0001F46C Найти людей в свой проект"
}

not_ready_yet = "\U00002639 Выбранный пункт меню пока не доступен"

user_not_registered_yet = "Пожалуйста, заполните анкету, чтобы продолжить"

enter_your_first_name = "Введите Ваше имя"

enter_your_last_name = "Введите Вашу фамилию"

enter_your_age = "Введите Ваш возраст"

enter_correct_age = "Пожалуйста, укажите возраст в виде целого неотрицательного числа"

enter_your_spoken_languages = "Укажите языки, которыми Вы владеете (можно указывать несколько)"

enter_your_programming_languages = "Укажите языки программирования, которыми Вы владеете (можно указывать несколько)"

enter_your_interests = "Укажите темы, которыми Вы интересуетесь (можно указывать несколько)"

do_not_specify = "\U0000274C Не хочу указывать"

finish_typing = '\U000027A1 Закончить и перейти на следующий пункт'

finish_registration = "\U0001F3C1 Регистрация завершена!"

your_profile = "\U0001F600 Ваш профиль:"

profile_items = {constants.ProfileItemsIds.FIRST_NAME: "Имя",
                 constants.ProfileItemsIds.LAST_NAME: "Фамилия",
                 constants.ProfileItemsIds.AGE: "Возраст",
                 constants.ProfileItemsIds.SPOKEN_LANGUAGES: "Языки",
                 constants.ProfileItemsIds.PROGRAMMING_LANGUAGES: "Языки программирования",
                 constants.ProfileItemsIds.INTERESTS: "Интересы"}

ok_edit = ["\U00002705 Всё верно", "\U0000270F Редактировать"]

select_from_the_list = "Пожалуйста, выберите один или несколько пунктов из списка"

call_main_menu = "/main_menu, чтобы перейти в главное меню бота"

user_have_not_search_parameters_yet = "Пожалуйста, укажите параметры для поиска единомышленников"

enter_age_group_for_search = "Выберите возрастные группы (можно указывать несколько)"

enter_spoken_languages = "Укажите языки (можно указывать несколько)"

enter_programming_languages = "Укажите языки программирования (можно указывать несколько)"

enter_interests = "Укажите интересы (можно указывать несколько)"

does_not_matter = "\U0000274C Не имеет значения"

finish_enter_search_parameters = "\U0001F3C1 Заполнение параметров для поиска единомышленников завершено!"

your_search_parameters = "Ваши параметры для поиска единомышленников:"

search_parameters_items = {constants.SearchParametersItemsIds.AGE_GROUP: "Возрастная группа",
                           constants.SearchParametersItemsIds.SPOKEN_LANGUAGES: "Языки",
                           constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES: "Языки программирования",
                           constants.SearchParametersItemsIds.INTERESTS: "Интересы"}

search_menu_title = "\U0001F50E Вы находитесь в меню поиска единомышленников"

values_of_search_menu_items = {
    constants.SearchMenuItems.FIND: "\U0001F50E Искать единомышленников",
    constants.SearchMenuItems.EDIT_SEARCH_PARAMETERS: "\U00002699 Редактировать параметры поиска",
    constants.SearchMenuItems.EDIT_PROFILE: "\U0001F600 Редактировать профиль"
}

get_contact = "\U0001F44D Начать общение"
skip_profile = "\U0001F50E Искать далее"
go_to_main_menu = "\U0001F3E0 Вернуться в главное меню"

candidates_profiles = "\U0001F4DC Профили согласно Вашим критериям поиска: "

telegram_login = "Telegram login: "

likes_blocked = "Вы исчерпали кол-во лайков, доступное бесплатно"

item_is_not_specified = "Не указано"

does_not_matter_without_emoji = "Не имеет значения"

no_profiles_more = "Вы просмотрели все профили, удовлетворяющие заданным критериям.\n\n\U000023F0 Новые профили будут появляться по мере роста популярности бота, поэтому проверяйте эту вкладку почаще!"

values_of_enums_constants = {
    constants.SpokenLanguages.RUSSIAN: "Русский",
    constants.SpokenLanguages.ENGLISH: "Английский",

    constants.ProgrammingLanguages.PYTHON: "Python",
    constants.ProgrammingLanguages.C: "C",
    constants.ProgrammingLanguages.CPP: "C++",
    constants.ProgrammingLanguages.C_SHARP: "C#",
    constants.ProgrammingLanguages.JAVA: "Java",
    constants.ProgrammingLanguages.JAVA_SCRIPT: "Java Script",
    constants.ProgrammingLanguages.SQL: "SQL",
    constants.ProgrammingLanguages.PHP: "PHP",
    constants.ProgrammingLanguages.SWIFT: "Swift",
    constants.ProgrammingLanguages.KOTLIN: "Kotlin",
    constants.ProgrammingLanguages.RUBY: "Ruby",
    constants.ProgrammingLanguages.ASSEMBLER: "Assembler",
    constants.ProgrammingLanguages.HTML_CSS: "HTML+CSS",
    constants.ProgrammingLanguages.NODE_JS: "Node.js",

    constants.Interests.DB_DESIGN: "Проектирование баз данных",
    constants.Interests.FRONT_END: "Front-end",
    constants.Interests.BACK_END: "Back-end",
    constants.Interests.MACHINE_LEARNING: "Machine learning",
    constants.Interests.BIG_DATA: "Big data",
    constants.Interests.DEV_FOR_ANDROID: "Разработка под Android",
    constants.Interests.DEV_FOR_IOS: "Разработка под iOS",
    constants.Interests.DESIGN: "Дизайн",
    constants.Interests.PROJECT_MANAGEMENT: "Управление проектами",
    constants.Interests.TESTING: "Тестирование",

    constants.AgeGroups.YOUNGER_THAN_14: "до 14 лет",
    constants.AgeGroups.FROM_14_TO_18: "от 14 до 18 лет",
    constants.AgeGroups.FROM_18_TO_25: "от 18 до 25 лет",
    constants.AgeGroups.OLDER_THAN_25: "старше 25 лет"
}

about_subscription = """\U0001F60E *Преимущества подписки:*\n- Cнятие ограничения на количество лайков\n- Продвижение вашего аккаунта на сервисе\n\n\U0001F4B3 Цена: *99 руб/мес*"""

buy = "\U0001F449 Купить!"

go_to_subscription_menu = "\U00002B50 Купить подписку"

press_btn_after_purchase = 'После покупки нажмите кнопку "Оплатил!"'
paid = "\U00002705 Оплатил!"

after_purchase = "\U0001F44D Спасибо за покупку!"
