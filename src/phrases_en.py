# File with phrases for the interface in Russian
import constants

welcome_message = "\U0001F44B Hi! I'm Practice Pals Bot.\nI'll help you find friends and future colleagues in IT."

main_menu_title = "\U0001F3E0 You're currently in main menu"

values_of_main_menu_items = {
    constants.MainMenuItems.FIND_PEOPLE: "\U0001F91D Find friends",
    constants.MainMenuItems.SUBSCRIPTION: "\U00002B50 Subscribe",
    constants.MainMenuItems.FIND_PROJECT: "\U0001F5C2 Find a project",
    constants.MainMenuItems.FIND_PEOPLE_TO_THE_PROJECT: "\U0001F46C Find people for your projects"
}

not_ready_yet = "\U00002639 Current option is temporary unavailable"

user_not_registered_yet = "\U0001F4DD Please fill the personal information to continue"

enter_your_first_name = "Enter your name"

enter_your_last_name = "Enter your last name"

enter_your_age = "Enter your age"

enter_correct_age = "Please enter your age as a non-negative number (0-99)"

enter_your_spoken_languages = "Choose the languages that you're familiar with (can choose multiple)"

enter_your_programming_languages = "Choose the programming languages that you're familiar with (can choose multiple)"

enter_your_interests = "Choose the topics that you're interested about"

do_not_specify = "\U0000274C Don't want to provide"

finish_typing = '\U000027A1 Go to the next section'

finish_registration = "\U0001F3C1 Registration complete!"

your_profile = "\U0001F600 Ваш профиль:"

profile_items = {constants.ProfileItemsIds.FIRST_NAME: "Name",
                 constants.ProfileItemsIds.LAST_NAME: "Last Name",
                 constants.ProfileItemsIds.AGE: "Age",
                 constants.ProfileItemsIds.SPOKEN_LANGUAGES: "Languages",
                 constants.ProfileItemsIds.PROGRAMMING_LANGUAGES: "Programmig languages",
                 constants.ProfileItemsIds.INTERESTS: "Interests"}

ok_edit = ["\U00002705 Correct", "\U0000270F Edit"]

user_have_not_search_parameters_yet = "Please choose the requirements for the people that you're looking for"

enter_age_group_for_search = "Choose the age group (can choose multiple)"

enter_spoken_languages = "Choose languges (can choose multiple)"

enter_programming_languages = "Choose the programming languages (can choose multiple)"

enter_interests = "Choose the interests (can choose multiple)"

does_not_matter = "\U0000274C Doesn't matter"

finish_enter_search_parameters = "\U0001F3C1 Done choosing the requiremnets!"

your_search_parameters = "\U00002699 Your requirements for the people:"

search_parameters_items = {constants.SearchParametersItemsIds.AGE_GROUP: "Age group",
                           constants.SearchParametersItemsIds.SPOKEN_LANGUAGES: "Languages",
                           constants.SearchParametersItemsIds.PROGRAMMING_LANGUAGES: "Programming languages",
                           constants.SearchParametersItemsIds.INTERESTS: "Interests"}

search_menu_title = "\U0001F50E You're in the search menu"

values_of_search_menu_items = {
    constants.SearchMenuItems.FIND: "\U0001F50E Find people",
    constants.SearchMenuItems.EDIT_SEARCH_PARAMETERS: "\U00002699 Edit searching requirements",
    constants.SearchMenuItems.EDIT_PROFILE: "\U0001F600 Edit profile",
    constants.SearchMenuItems.GO_TO_MAIN_MENU: "\U0001F3E0 Go back to the main mane"
}

go_to_main_menu = "\U0001F3E0 Go back to the main mane"

candidates_profiles = "\U0001F4DC Here're the profiles that fit your requirements: "

telegram_login = "Telegram login: "

likes_blocked = "You're out of free likes"

item_is_not_specified = "Not specifies"

does_not_matter_without_emoji = "Doesn't matter"

no_profiles_more = "These were all the profiles that fit your requirements.\n\n\U000023F0 Check this section a bit later!"

values_of_possible_answers = {
    constants.SpokenLanguages.RUSSIAN: "Russian",
    constants.SpokenLanguages.ENGLISH: "English",

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

    constants.Interests.DB_DESIGN: "Database design",
    constants.Interests.FRONT_END: "Front-end",
    constants.Interests.BACK_END: "Back-end",
    constants.Interests.MACHINE_LEARNING: "Machine learning",
    constants.Interests.BIG_DATA: "Big data",
    constants.Interests.DEV_FOR_ANDROID: "Android Development",
    constants.Interests.DEV_FOR_IOS: "iOS Development",
    constants.Interests.DESIGN: "Design",
    constants.Interests.PROJECT_MANAGEMENT: "Project Management",
    constants.Interests.TESTING: "Testing",

    constants.AgeGroups.YOUNGER_THAN_14: "less than 14 years old",
    constants.AgeGroups.FROM_14_TO_18: "from 14 to 18 years old",
    constants.AgeGroups.FROM_18_TO_25: "from 18 to 25 years old",
    constants.AgeGroups.OLDER_THAN_25: "more that 25 years old"
}

about_subscription = """\U0001F60E *Why you should consider subscribing:*\n- unlimited likes\n- Higher priority for your profile\n\n\U0001F4B3 Price: 2$/month*"""

buy = "\U0001F449 Subscribe!"

go_to_subscription_menu = "\U00002B50 Subscribe"

press_btn_after_purchase = 'Please press "Subscribed!" button after purchasing'
paid = "\U00002705 Subscribed!"

after_purchase = "\U0001F44D Thanks for your support!"

we_ask_personal_data = "\U00002755 For better precicion of the search algorithms you may fill up your personal info (name, last name, email).\n\n We don't share that data with third party and only use it internally in the bot.\n\n\U00002754 Do you agree with us storing the data? (If not, you can just not specity specific data)"

personal_data_you_agree = "\U00002705 You agreed to store the data"
personal_data_you_refuse = "\U0000274C You didn't agree to store the data"

profile_reaction_menu_items = {
    constants.ProfileReactionsMenu.LIKE: "\U0001F44D Start talking",
    constants.ProfileReactionsMenu.SKIP: "\U0001F50E Keep looking",
    constants.ProfileReactionsMenu.GO_TO_MAIN_MENU: "\U0001F3E0 back to main menu",
}

ask_personal_data_menu_items = {
    constants.AskPersonalData.AGREE: "\U00002705 Agree",
    constants.AskPersonalData.REFUSE: "\U0000274C Refuse"
}

after_choice = '\U000027A1 After choosing all the requirements press "Go to the next section"'

edit_profile_menu = "\U0000270F You're editing the profile"

select_the_profile_item_to_edit = "\U0001F600 Choose the data that you want to edit"

edit_search_parameters_menu = "\U0000270F You're editing the search parameters"

select_the_search_parameters_item_to_edit = "\U00002699 Choose the search parameter that you want to edit"
