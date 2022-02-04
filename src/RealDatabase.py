from sqlalchemy import *
from typing import Optional

import choice_fields as mp # multiple choice
from database_constants import *
from constants import MenuIds, SearchParametersItemsIds, ProfileItemsIds
from IDatabase import IDatabase

class Database(IDatabase):
    def __init__(self):
        self.engine = create_engine('sqlite:///testdb.db', echo=True)
        self.metadata = MetaData()

        self.Account = Table(
            'Account',
            self.metadata,
            Column(ID, Integer, primary_key=True),
            Column(TELEGRAM_LOGIN, String(255), unique=True, nullable=False),
            Column(TELEGRAM_ID, Integer, nullable=False, unique=True),

            Column(IS_REGISTERED, Boolean, nullable=False, default=False),
            Column(ARE_SEARCH_PARAMETERS_FILLED, Boolean, nullable=False, default=False),

            Column(NUMBER_OF_LIKES, Integer, nullable=False, default=0),
            Column(LAST_PROFILE_ID, Integer)
        )

        self.Navigation = Table(
            'Navigation',
            self.metadata,
            Column(ID, Integer, primary_key=True),
            Column(TELEGRAM_ID, ForeignKey('Account.telegram_id'), unique=True), 
            Column(MENU_ID, Enum(MenuIds), nullable=False),
            Column(REGISTRATION_ITEM_ID, Enum(ProfileItemsIds), nullable=False),
            Column(SEARCH_PARAMETER_ITEM_ID, Enum(SearchParametersItemsIds), nullable=False)
        )

        self.PotentialProfiles = Table(
            'PotentialProfiles',
            self.metadata,
            Column(ID, Integer, primary_key=True),
            Column(TELEGRAM_ID, ForeignKey('Account.telegram_id')), 
            Column(SENDER_ACCOUNT_ID, Integer, nullable=False),
            Column(REQUESTED_ACCOUNT_ID, Integer, nullable=False), 
            Column(IS_VIEWED, Boolean, nullable=False, default=False)
        )

        self.SearchParameters = Table(
            'SearchParameters',
            self.metadata,
            Column(ID, Integer, primary_key=True),
            Column(TELEGRAM_ID, ForeignKey('Account.telegram_id'), unique=True), 
            Column(AGE, Enum(mp.PreferedAge)),
            Column(SPOKEN_LANGUAGES, Enum(mp.SpokenLanguages)),
            Column(PROGRAMMING_LANGUAGES, Enum(mp.ProgrammingLanguages)),
        )

        self.Profile = Table(
            'Profile',
            self.metadata,
            Column(ID, Integer, primary_key=True),
            Column(TELEGRAM_ID, ForeignKey('Account.telegram_id'), unique=True), 
            Column(FIRST_NAME, String(255), nullable=False),
            Column(LAST_NAME, String(255)),
            Column(AGE, Integer),
            Column(PHOTO_URL, String(255)),
            Column(SPOKEN_LANGUAGES, Enum(mp.SpokenLanguages)),
            Column(PROGRAMMING_LANGUAGES, Enum(mp.ProgrammingLanguages)),
        )

        self.metadata.create_all(self.engine)
        self.connection = self.engine.connect()

    def is_registered(self, user_id: int):
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
        

    def get_users_menu_id(self, user_id: int) -> MenuIds:
        statement = select(
            self.Navigation.c[MENU_ID]
        ).where(self.Navigation.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()
        
        return mapped_result.scalars().all()[0]


    def set_users_menu_id(self, user_id: int, new_menu_id: MenuIds) -> None:
        statement = update(
            self.Navigation
        ).where(self.Navigation.c[TELEGRAM_ID] == user_id).values({MENU_ID: new_nenu_id})

        result = self.connection.execute(statement)


    def get_users_registration_item_id(self, user_id: int) -> ProfileItemsIds:
        statement = select(
            self.Navigation.c[REGISTRATION_ITEM_ID]
        ).where(self.Navigation.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()
        
        return mapped_result.scalars().all()[0]


    def set_users_registration_item_id(self, user_id: int, new_registration_item_id: ProfileItemsIds) -> None:
        statement = update(
            self.Navigation
        ).where(self.Navigation.c[TELEGRAM_ID] == user_id).values({REGISTRATION_ITEM_ID: new_registration_item_id})

        result = self.connection.execute(statement)


    def get_users_profile_item(self, user_id: int, item: str) -> Optional[str]:
        statement = select(
            self.Profile.c[item]
        ).where(self.Profile.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()
        
        return mapped_result.scalars().all()[0]

    
    def set_users_profile_item(self, user_id: int, item: str, value: Optional[str]) -> None:
        statement = update(
            self.Profile.c[item]
        ).where(self.Profile.c[TELEGRAM_ID] == user_id).values({item: value})

        result = self.connection.execute(statement)


    def append_to_users_profile_item(self, user_id: int, item: ProfileItemsIds, value: str) -> None:
        pass


    def are_search_parameters_filled(self, user_id: int) -> bool:
        statement = select(
            self.Account.c[ARE_SEARCH_PARAMETERS_FILLED]
        ).where(self.Account.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()
        
        return mapped_result.scalars().all()[0]


    def set_search_parameters_filled(self, user_id: int) -> None:
        statement = update(
            self.Account
        ).where(self.Account.c[TELEGRAM_ID] == user_id).values({ARE_SEARCH_PARAMETERS_FILLED: True})

        result = self.connection.execute(statement)


    def get_users_search_parameter_item_id(self, user_id: int) -> SearchParametersItemsIds:
        statement = select(
            self.Account.c[ARE_SEARCH_PARAMETERS_FILLED]
        ).where(self.Account.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()
        
        return mapped_result.scalars().all()[0]


    def set_users_search_parameter_item_id(self, user_id: int, new_search_parameter_item_id: SearchParametersItemsIds) -> None:
        statement = update(
            self.Navigation
        ).where(self.Navigation.c[TELEGRAM_ID] == user_id).values({SEARCH_PARAMETER_ITEM_ID: new_search_parameter_item_id})
        
        result = self.connection.execute(statement)


    def get_users_search_parameter_item(self, user_id: int, item: str) -> Optional[str]:
        statement = select(
            self.Navigation.c[item]
        ).where(self.Navigation.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()
        
        return mapped_result.scalars().all()[0]


    def append_to_users_search_parameter_item(self, user_id: int, item: SearchParametersItemsIds, value: Optional[str]) -> None:
        pass

    def get_users_last_shown_profile_id(self, user_id: int) -> Optional[int]:
        statement = select(
            self.Account.c[LAST_PROFILE_ID]
        ).where(self.Account.c[TELEGRAM_ID] == user_id)

        result = self.connection.execute(statement)
        mapped_result = result.scalars().all()
        
        return mapped_result.scalars().all()[0]


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


DATABASE = Database()

