# File with phrases for the interface in Russian
import constants

welcome_message = "Привет! Я Practice Pals Bot. Помогу Вам найти друзей по интересам в IT-сфере"

main_menu_title = "Вы находитесь в главном меню бота"

main_menu_list = ["\U0001F91D Найти единомышленников",
                  "\U0001F5C2 Найти проект",
                  "\U0001F46C Найти людей в свой проект"]

not_ready_yet = "Выбранный пункт меню пока не доступен :("

user_not_registered_yet = "Похоже, Вы пользуйтесь этим ботом первый раз. Пожалуйста, запоните данные о себе, чтобы продолжить"

enter_your_first_name = "Введите Ваше имя"

enter_your_last_name = "Введите Вашу фамилию"

enter_your_age = "Введите Ваш возраст"

enter_your_spoken_languages = "Укажите языки, которыми Вы владеете (можно указывать несколько)"

enter_your_programming_languages = "Укажите языки программирования, которыми Вы владеете (можно указывать несколько)"

enter_your_interests = "Укажите темы, которыми Вы интересуетесь"

do_not_specify = "\U0000274C Не хочу указывать"

spoken_languages = ["Русский", "Английский"]

programming_languages = ["Python", "C", "C++", "Java"]

interests = ["Front-end", "Back-end", "ML", "Big Data"]

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
