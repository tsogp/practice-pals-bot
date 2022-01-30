from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

import choice_fields as mp # multiple choice
import constants
import IDatabase

class DB(IDatabase):
    def __init__(self):
        self.metadata = MetaData()
        self.engine = create_engine('sqlite:///testdb.db', echo=True)

        self.account = Table(
            'Account',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('telegram_login', String(255), unique=True, nullable=False),
            Column('telegram_id', Integer, nullable=False, unique=True),


            Column('is_registered', Boolean, nullable=False, default=False),
            Column('are_search_parameters_filled', Boolean, nullable=False, default=False),

            # relationship needed
            Column('navigation_id', ForeignKey('Navigation.id')), 
            Column('profile_id', ForeignKey('Profile.id')),
            Column('search_parameters_id', ForeignKey('SearchParameters.id')),
            Column('potential_relationship_id', ForeignKey('PotentialProfiles.id')),

            Column('number_of_likes', Integer, nullable=False, default=0),
            Column('last_profile_id', Integer)
        )

        self.navigation = Table(
            'Navigation',
            self.matadata,
            Column('id', Integer, primary_key=True),
            Column('menu_id', Enum(constants.MenuIds), nullable=False),
            Column('registration_item_id', Enum(constants.ProfileItemsIds), nullable=False),
            Column('search_parameter_item_id', Enum(constants.SearchParametersItemsIds), nullable=False)
        )

        self.potentialprofiles = Table(
            'PotentialProfiles',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('sender_account_id', Integer, nullable=False),
            Column('requested_account_id', Integer, nullable=False), 
            Column('is_viewed', Boolean, nullable=False, default=False)
        )

        self.searchparameters = Table(
            'SearchParameters',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('age', Enum(mp.PreferedAge)),
            Column('spoken_languages', Enum(mp.SpokenLanguages)),
            Column('programming_languages', Enum(mp.ProgrammingLanguages)),
        )

        self.profile = Table(
            'Profile',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('first_name', String(255), nullable=False),
            Column('last_name', String(255)),
            Column('age', Integer),
            Column('photo_url', String(255), unique=True),
            Column('spoken_languages', Enum(mp.SpokenLanguages)),
            Column('programming_languages', Enum(mp.ProgrammingLanguages)),
            Column('about_me', String(2000))
        )

        self.metadata.create_all(self.engine)

        
    def is_registered(self, user_id: int) -> bool:
        pass

    def register_user(self, user_id: int) -> None:
        pass

    def get_users_menu_id(self, user_id: int) -> constants.MenuIds:
        pass

    def set_users_menu_id(self, user_id: int, new_menu_id: constants.MenuIds) -> None:
        pass

    def get_users_registration_item_id(self, user_id: int) -> constants.ProfileItemsIds:
        pass

    def set_users_registration_item_id(self, user_id: int, new_registration_item_id: constants.ProfileItemsIds) -> None:
        pass

    def get_users_profile_item(self, user_id: int, item: constants.ProfileItemsIds) -> Optional[str]:
        pass

    def set_users_profile_item(self, user_id: int, item: constants.ProfileItemsIds, value: Optional[str]) -> None:
        pass

    def append_to_users_profile_item(self, user_id: int, item: constants.ProfileItemsIds, value: str) -> None:
        pass

    def are_search_parameters_filled(self, user_id: int) -> None:
        pass

    def set_search_parameters_filled(self, user_id: int) -> None:
        pass

    def get_users_search_parameter_item_id(self, user_id: int) -> constants.SearchParametersItemsIds:
        pass

    def set_users_search_parameter_item_id(self, user_id: int,
                                        new_search_parameter_item_id: constants.SearchParametersItemsIds) -> None:
        pass

    def get_users_search_parameter_item(self, user_id: int, item: constants.SearchParametersItemsIds) -> Optional[str]:
        pass

    def append_to_users_search_parameter_item(self, user_id: int, item: constants.SearchParametersItemsIds,
                                            value: Optional[str]) -> None:
        pass

    def get_users_last_shown_profile_id(self, user_id: int) -> Optional[int]:
        pass

    def set_users_last_shown_profile_id(self, user_id: int, candidate_id: int) -> None:
        pass
    
    def get_users_telegram_login_by_id(self, user_id: int) -> str:
        pass

    def get_number_of_likes(self, user_id: int) -> int:
        pass

    def inc_number_of_likes(self, user_id: int) -> None:
        pass

DATABASE = DB()

