from sqlalchemy import *
from typing import Optional, List

import choice_fields as mp  # multiple choice
from database_constants import *
import constants
from IDatabase import IDatabase


class Database(IDatabase):
    def __init__(self):
        self.engine = create_engine(
            'sqlite:///testdb.db',
            echo=False,
            connect_args={'check_same_thread': False}
        )

        self.metadata = MetaData()

        self.Account = Table(
            'Account',
            self.metadata,
            Column(ID, Integer, primary_key=True),
            Column(TELEGRAM_LOGIN, String(255), unique=True),
            Column(TELEGRAM_ID, Integer, unique=True),

            Column(IS_REGISTERED, Boolean, default=False),
            Column(ARE_SEARCH_PARAMETERS_FILLED, Boolean, default=False),

            Column(NUMBER_OF_LIKES, Integer, default=0),
            Column(LAST_PROFILE_ID, Integer, default=None),
            Column(IS_SUBSCRIBED, Boolean, default=False)
        )

        self.Navigation = Table(
            'Navigation',
            self.metadata,
            Column(ID, Integer, primary_key=True),
            Column(TELEGRAM_ID, ForeignKey('Account.telegram_id'), unique=True),
            Column(MENU_ID, Enum(constants.MenuIds), default=constants.MenuIds.NULL),
            Column(REGISTRATION_ITEM_ID, Enum(constants.ProfileItemsIds), default=constants.ProfileItemsIds.NULL),
            Column(SEARCH_PARAMETER_ITEM_ID, Enum(constants.SearchParametersItemsIds),
                   default=constants.SearchParametersItemsIds.NULL)
        )

        self.PotentialProfiles = Table(
            'PotentialProfiles',
            self.metadata,
            Column(ID, Integer, primary_key=True),
            Column(TELEGRAM_ID, ForeignKey('Account.telegram_id')),
            Column(SENDER_ACCOUNT_ID, Integer, default=None),
            Column(REQUESTED_ACCOUNT_ID, Integer, default=None),
            Column(IS_VIEWED, Boolean, default=False)
        )

        self.SearchParameters = Table(
            'SearchParameters',
            self.metadata,
            Column(ID, Integer, primary_key=True),
            Column(TELEGRAM_ID, ForeignKey('Account.telegram_id'), unique=True),

            # Spoken Languages
            Column(RUSSIAN, Boolean, default=False),
            Column(ENGLISH, Boolean, default=False),

            # Programming Languages
            Column(PYTHON, Boolean, default=False),
            Column(C, Boolean, default=False),
            Column(CPP, Boolean, default=False),
            Column(C_SHARP, Boolean, default=False),
            Column(JAVA, Boolean, default=False),
            Column(JAVA_SCRIPT, Boolean, default=False),
            Column(SQL, Boolean, default=False),
            Column(PHP, Boolean, default=False),
            Column(SWIFT, Boolean, default=False),
            Column(KOTLIN, Boolean, default=False),
            Column(RUBY, Boolean, default=False),
            Column(ASSEMBLER, Boolean, default=False),
            Column(HTML_CSS, Boolean, default=False),
            Column(NODE_JS, Boolean, default=False),

            # Interests
            Column(DB_DESIGN, Boolean, default=False),
            Column(FRONT_END, Boolean, default=False),
            Column(BACK_END, Boolean, default=False),
            Column(MACHINE_LEARNING, Boolean, default=False),
            Column(BIG_DATA, Boolean, default=False),
            Column(DEV_FOR_ANDROID, Boolean, default=False),
            Column(DEV_FOR_IOS, Boolean, default=False),
            Column(DESIGN, Boolean, default=False),
            Column(PROJECT_MANAGEMENT, Boolean, default=False),
            Column(TESTING, Boolean, default=False),

            # Age groups
            Column(YOUNGER_THAN_14, Boolean, default=False),
            Column(FROM_14_TO_18, Boolean, default=False),
            Column(FROM_18_TO_25, Boolean, default=False),
            Column(OLDER_THAN_25, Boolean, default=False)
        )

        self.Profile = Table(
            'Profile',
            self.metadata,
            Column(ID, Integer, primary_key=True),
            Column(TELEGRAM_ID, ForeignKey('Account.telegram_id'), unique=True),
            Column(FIRST_NAME, String(255), default=None),
            Column(LAST_NAME, String(255), default=None),
            Column(AGE, Integer, default=None),
            Column(PHOTO_URL, String(255), default=None),

            # Spoken Languages
            Column(RUSSIAN, Boolean, default=False),
            Column(ENGLISH, Boolean, default=False),

            # Programming Languages
            Column(PYTHON, Boolean, default=False),
            Column(C, Boolean, default=False),
            Column(CPP, Boolean, default=False),
            Column(C_SHARP, Boolean, default=False),
            Column(JAVA, Boolean, default=False),
            Column(JAVA_SCRIPT, Boolean, default=False),
            Column(SQL, Boolean, default=False),
            Column(PHP, Boolean, default=False),
            Column(SWIFT, Boolean, default=False),
            Column(KOTLIN, Boolean, default=False),
            Column(RUBY, Boolean, default=False),
            Column(ASSEMBLER, Boolean, default=False),
            Column(HTML_CSS, Boolean, default=False),
            Column(NODE_JS, Boolean, default=False),

            # Interests
            Column(DB_DESIGN, Boolean, default=False),
            Column(FRONT_END, Boolean, default=False),
            Column(BACK_END, Boolean, default=False),
            Column(MACHINE_LEARNING, Boolean, default=False),
            Column(BIG_DATA, Boolean, default=False),
            Column(DEV_FOR_ANDROID, Boolean, default=False),
            Column(DEV_FOR_IOS, Boolean, default=False),
            Column(DESIGN, Boolean, default=False),
            Column(PROJECT_MANAGEMENT, Boolean, default=False),
            Column(TESTING, Boolean, default=False)
        )

        self.metadata.create_all(self.engine)
        self.connection = self.engine.connect()

    def initial_user_setup(self, user_id: int) -> None:
        statement = insert(
            self.Account,
        ).values({TELEGRAM_ID: user_id})

        result = self.connection.execute(statement)

        statement = insert(
            self.Navigation,
        ).values({TELEGRAM_ID: user_id})

        result = self.connection.execute(statement)

        statement = insert(
            self.SearchParameters,
        ).values({TELEGRAM_ID: user_id})

        result = self.connection.execute(statement)

        statement = insert(
            self.Profile,
        ).values({TELEGRAM_ID: user_id})

        result = self.connection.execute(statement)

    def is_in_database(self, user_id: int) -> bool:
        statement = select(
            self.Account.c[TELEGRAM_ID]
        ).where(self.Account.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()

        return bool(mapped_result)

    def is_registered(self, user_id: int) -> bool:
        statement = select(
            self.Account.c[IS_REGISTERED]
        ).where(self.Account.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()

        return mapped_result[0]

    def register_user(self, user_id: int) -> None:
        statement = update(
            self.Account
        ).where(self.Account.c[TELEGRAM_ID] == user_id).values({IS_REGISTERED: True})

        result = self.connection.execute(statement)

    def get_users_menu_id(self, user_id: int) -> Optional[constants.MenuIds]:
        statement = select(
            self.Navigation.c[MENU_ID]
        ).where(self.Navigation.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()

        if not mapped_result:
            return None

        return mapped_result[0]

    def set_users_menu_id(self, user_id: int, new_menu_id: constants.MenuIds) -> None:
        statement = update(
            self.Navigation
        ).where(self.Navigation.c[TELEGRAM_ID] == user_id).values({MENU_ID: new_menu_id})

        result = self.connection.execute(statement)

    def get_users_registration_item_id(self, user_id: int) -> Optional[constants.ProfileItemsIds]:
        statement = select(
            self.Navigation.c[REGISTRATION_ITEM_ID]
        ).where(self.Navigation.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()

        if not mapped_result:
            return None

        return mapped_result[0]

    def set_users_registration_item_id(self, user_id: int, new_registration_item_id: constants.ProfileItemsIds) -> None:
        statement = update(
            self.Navigation
        ).where(self.Navigation.c[TELEGRAM_ID] == user_id).values({REGISTRATION_ITEM_ID: new_registration_item_id})

        result = self.connection.execute(statement)

    def get_users_profile_first_name(self, user_id: int) -> str:
        statement = select(
            self.Profile.c[FIRST_NAME]
        ).where(self.Profile.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()

        return mapped_result[0]

    def set_users_profile_first_name(self, user_id: int, value: str) -> None:
        statement = update(
            self.Profile
        ).where(self.Profile.c[TELEGRAM_ID] == user_id).values({FIRST_NAME: value})

        result = self.connection.execute(statement)

    def get_users_profile_last_name(self, user_id: int) -> str:
        statement = select(
            self.Profile.c[LAST_NAME]
        ).where(self.Profile.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()

        return mapped_result[0]

    def set_users_profile_last_name(self, user_id: int, value: str) -> None:
        statement = update(
            self.Profile
        ).where(self.Profile.c[TELEGRAM_ID] == user_id).values({LAST_NAME: value})

        result = self.connection.execute(statement)

    def get_users_profile_age(self, user_id: int) -> int:
        statement = select(
            self.Profile.c[AGE]
        ).where(self.Profile.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()

        return mapped_result[0]

    def set_users_profile_age(self, user_id: int, value: int) -> None:
        statement = update(
            self.Profile
        ).where(self.Profile.c[TELEGRAM_ID] == user_id).values({AGE: value})

        result = self.connection.execute(statement)

    def get_users_profile_spoken_languages(self, user_id: int) -> List[constants.SpokenLanguages]:
        mapped_result = []

        for column in SPOKEN_LANGUAGES_LIST:
            statement = select(
                self.Profile.c[column]
            ).where(self.Profile.c[TELEGRAM_ID] == user_id)

            result = self.connection.execute(statement)
            if result.scalars().all()[0]:
                mapped_result.append(constants.SpokenLanguages(column))

        return mapped_result

    def append_to_users_profile_spoken_languages(self, user_id: int, value: constants.SpokenLanguages) -> None:
        statement = update(
            self.Profile
        ).where(self.Profile.c[TELEGRAM_ID] == user_id).values({value.value: True})

        result = self.connection.execute(statement)

    def set_users_profile_spoken_languages_null(self, user_id: int) -> None:
        for column in SPOKEN_LANGUAGES_LIST:
            statement = update(
                self.Profile
            ).where(self.Profile.c[TELEGRAM_ID] == user_id).values({column: False})

            result = self.connection.execute(statement)

    def get_users_profile_programming_languages(self, user_id: int) -> List[constants.ProgrammingLanguages]:
        mapped_result = []

        for column in PROGRAMMING_LANGUAGES_LIST:
            statement = select(
                self.Profile.c[column]
            ).where(self.Profile.c[TELEGRAM_ID] == user_id)

            result = self.connection.execute(statement)
            if result.scalars().all()[0]:
                mapped_result.append(constants.ProgrammingLanguages(column))

        return mapped_result

    def append_to_users_profile_programming_languages(self, user_id: int,
                                                      value: constants.ProgrammingLanguages) -> None:
        statement = update(
            self.Profile
        ).where(self.Profile.c[TELEGRAM_ID] == user_id).values({value.value: True})

        result = self.connection.execute(statement)

    def set_users_profile_programming_languages_null(self, user_id: int) -> None:
        for column in PROGRAMMING_LANGUAGES_LIST:
            statement = update(
                self.Profile
            ).where(self.Profile.c[TELEGRAM_ID] == user_id).values({column: None})

            result = self.connection.execute(statement)

    def get_users_profile_interests(self, user_id: int) -> List[constants.Interests]:
        mapped_result = []

        for column in INTERESTS_LIST:
            statement = select(
                self.Profile.c[column]
            ).where(self.Profile.c[TELEGRAM_ID] == user_id)

            result = self.connection.execute(statement)
            if result.scalars().all()[0]:
                mapped_result.append(constants.Interests(column))

        return mapped_result

    def append_to_users_profile_interests(self, user_id: int, value: constants.Interests) -> None:
        statement = update(
            self.Profile
        ).where(self.Profile.c[TELEGRAM_ID] == user_id).values({value.value: True})

        result = self.connection.execute(statement)

    def set_users_profile_interests_null(self, user_id: int) -> None:
        for column in INTERESTS_LIST:
            statement = update(
                self.Profile
            ).where(self.Profile.c[TELEGRAM_ID] == user_id).values({column: None})

            result = self.connection.execute(statement)

    def are_search_parameters_filled(self, user_id: int) -> bool:
        statement = select(
            self.Account.c[ARE_SEARCH_PARAMETERS_FILLED]
        ).where(self.Account.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()

        return mapped_result[0]

    def set_search_parameters_filled(self, user_id: int) -> None:
        statement = update(
            self.Account
        ).where(self.Account.c[TELEGRAM_ID] == user_id).values({ARE_SEARCH_PARAMETERS_FILLED: True})

        result = self.connection.execute(statement)

    def get_users_search_parameter_item_id(self, user_id: int) -> Optional[constants.SearchParametersItemsIds]:
        statement = select(
            self.Navigation.c[SEARCH_PARAMETER_ITEM_ID]
        ).where(self.Navigation.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()

        if not mapped_result:
            return None

        return mapped_result[0]

    def set_users_search_parameters_item_id(self, user_id: int,
                                            new_search_parameter_item_id: constants.SearchParametersItemsIds) -> None:
        statement = update(
            self.Navigation
        ).where(self.Navigation.c[TELEGRAM_ID] == user_id).values(
            {SEARCH_PARAMETER_ITEM_ID: new_search_parameter_item_id})

        result = self.connection.execute(statement)

    def get_users_search_parameters_age_groups(self, user_id: int) -> List[constants.AgeGroups]:
        mapped_result = []

        for column in AGE_GROUP_LIST:
            statement = select(
                self.SearchParameters.c[column]
            ).where(self.SearchParameters.c[TELEGRAM_ID] == user_id)

            result = self.connection.execute(statement)
            if result.scalars().all()[0]:
                mapped_result.append(constants.AgeGroups(column))

        return mapped_result

    def append_to_users_search_parameters_age_groups(self, user_id: int, value: constants.AgeGroups) -> None:
        statement = update(
            self.SearchParameters
        ).where(self.SearchParameters.c[TELEGRAM_ID] == user_id).values({value.value: True})

        result = self.connection.execute(statement)

    def set_users_profile_search_parameters_age_groups_null(self, user_id: int) -> None:
        for column in AGE_GROUP_LIST:
            statement = update(
                self.SearchParameters
            ).where(self.SearchParameters.c[TELEGRAM_ID] == user_id).values({column: None})

            result = self.connection.execute(statement)

    def get_users_search_parameters_spoken_languages(self, user_id: int) -> List[constants.SpokenLanguages]:
        mapped_result = []

        for column in SPOKEN_LANGUAGES_LIST:
            statement = select(
                self.SearchParameters.c[column]
            ).where(self.SearchParameters.c[TELEGRAM_ID] == user_id)

            result = self.connection.execute(statement)
            if result.scalars().all()[0]:
                mapped_result.append(constants.SpokenLanguages(column))

        return mapped_result

    def append_to_users_search_parameters_spoken_languages(self, user_id: int,
                                                           value: constants.SpokenLanguages) -> None:
        statement = update(
            self.SearchParameters
        ).where(self.SearchParameters.c[TELEGRAM_ID] == user_id).values({value.value: True})

        result = self.connection.execute(statement)

    def set_users_profile_search_parameters_spoken_languages_null(self, user_id: int) -> None:
        for column in SPOKEN_LANGUAGES_LIST:
            statement = update(
                self.SearchParameters
            ).where(self.SearchParameters.c[TELEGRAM_ID] == user_id).values({column: None})

            result = self.connection.execute(statement)

    def get_users_search_parameters_programming_languages(self, user_id: int) -> List[constants.ProgrammingLanguages]:
        mapped_result = []

        for column in PROGRAMMING_LANGUAGES_LIST:
            statement = select(
                self.SearchParameters.c[column]
            ).where(self.SearchParameters.c[TELEGRAM_ID] == user_id)

            result = self.connection.execute(statement)
            if result.scalars().all()[0]:
                mapped_result.append(constants.ProgrammingLanguages(column))
        return mapped_result

    def append_to_users_search_parameters_programming_languages(self, user_id: int,
                                                                value: constants.ProgrammingLanguages) -> None:
        statement = update(
            self.SearchParameters
        ).where(self.SearchParameters.c[TELEGRAM_ID] == user_id).values({value.value: True})

        result = self.connection.execute(statement)

    def set_users_profile_search_parameters_programming_languages_null(self, user_id: int) -> None:
        for column in PROGRAMMING_LANGUAGES_LIST:
            statement = update(
                self.SearchParameters
            ).where(self.SearchParameters.c[TELEGRAM_ID] == user_id).values({column: None})

            result = self.connection.execute(statement)

    def get_users_search_parameters_interests(self, user_id: int) -> List[constants.Interests]:
        mapped_result = []

        for column in INTERESTS_LIST:
            statement = select(
                self.SearchParameters.c[column]
            ).where(self.SearchParameters.c[TELEGRAM_ID] == user_id)

            result = self.connection.execute(statement)
            if result.scalars().all()[0]:
                mapped_result.append(constants.Interests(column))

        return mapped_result

    def append_to_users_search_parameters_interests(self, user_id: int, value: constants.Interests) -> None:
        statement = update(
            self.SearchParameters
        ).where(self.SearchParameters.c[TELEGRAM_ID] == user_id).values({value.value: True})

        result = self.connection.execute(statement)

    def set_users_profile_search_parameters_interests_null(self, user_id: int) -> None:
        for column in INTERESTS_LIST:
            statement = update(
                self.SearchParameters
            ).where(self.SearchParameters.c[TELEGRAM_ID] == user_id).values({column: None})

            result = self.connection.execute(statement)

    def get_users_last_shown_profile_id(self, user_id: int) -> Optional[int]:
        statement = select(
            self.Account.c[LAST_PROFILE_ID]
        ).where(self.Account.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()

        return mapped_result[0]

    def set_users_last_shown_profile_id(self, user_id: int, candidate_id: int) -> None:
        statement = update(
            self.Account
        ).where(self.Account.c[TELEGRAM_ID] == user_id).values({LAST_PROFILE_ID: candidate_id})

        result = self.connection.execute(statement)

    def get_users_telegram_login_by_id(self, user_id: int) -> str:
        statement = select(
            self.Account.c[TELEGRAM_LOGIN]
        ).where(self.Account.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()

        return mapped_result[0]

    def get_number_of_likes(self, user_id: int) -> int:
        statement = select(
            self.Account.c[NUMBER_OF_LIKES]
        ).where(self.Account.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()

        return mapped_result[0]

    def inc_number_of_likes(self, user_id: int) -> None:
        current_number_of_likes = self.get_number_of_likes(user_id)

        statement = update(
            self.Account
        ).where(self.Account.c[TELEGRAM_ID] == user_id).values({NUMBER_OF_LIKES: current_number_of_likes + 1})

        result = self.connection.execute(statement)

    def have_subscription(self, user_id: int) -> bool:
        statement = select(
            self.Account.c[IS_SUBSCRIBED]
        ).where(self.Account.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()

        return mapped_result[0]

    def add_candidate(self, user_id: int, candidate_id: int) -> None:
        statement = update(
            self.PotentialProfiles
        ).where(self.PotentialProfiles.c[TELEGRAM_ID] == user_id).values({REQUESTED_ACCOUNT_ID: candidate_id})

        result = self.connection.execute(statement)

    def get_not_viewed_candidates(self, user_id: int) -> Optional[List[int]]:
        statement = select(
            self.PotentialProfiles.c[ID]
        ).where(
            and_(self.PotentialProfiles.c[SENDER_ACCOUNT_ID] == user_id, self.PotentialProfiles.c[IS_VIEWED] == False))

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()

        return mapped_result

    def mark_profile_as_viewed(self, user_id: int, candidate_id: int) -> None:
        statement = update(
            self.PotentialProfiles
        ).where(and_(self.PotentialProfiles.c[SENDER_ACCOUNT_ID] == user_id,
                     self.PotentialProfiles.c[REQUESTED_ACCOUNT_ID] == candidate_id)
                ).values({IS_VIEWED: True})

        result = self.connection.execute(statement)

    def is_profile_viewed(self, user_id: int, candidate_id: int) -> bool:
        statement = select(
            self.PotentialProfiles.c[IS_VIEWED]
        ).where(and_(self.PotentialProfiles.c[SENDER_ACCOUNT_ID] == user_id,
                     self.PotentialProfiles.c[REQUESTED_ACCOUNT_ID] == candidate_id))

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()

        return mapped_result[0]

    def get_all_users(self) -> List[int]:
        statement = select(
            self.Account.c[TELEGRAM_ID]
        )

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()

        return mapped_result

    def activate_subscription(self, user_id: int) -> None:
        pass

    def deactivate_subscription(self, user_id: int) -> None:
        pass

# DATABASE = Database()
