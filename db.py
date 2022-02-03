from sqlalchemy import *
from typing import Optional

import choice_fields as mp # multiple choice
import constants
from IDatabase import IDatabase

class DB(IDatabase):
    def __init__(self):
        self.engine = create_engine('sqlite:///testdb.db', echo=True)
        self.metadata = MetaData(bind=self.engine)

        self.Account = Table(
            'Account',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('telegram_login', String(255), unique=True, nullable=False),
            Column('telegram_id', Integer, nullable=False, unique=True),


            Column('is_registered', Boolean, nullable=False, default=False),
            Column('are_search_parameters_filled', Boolean, nullable=False, default=False),

            # # relationship needed
            # Column('profile_id', ForeignKey('Profile.id')),
            # Column('search_parameters_id', ForeignKey('SearchParameters.id')),
            # Column('potential_relationship_id', ForeignKey('PotentialProfiles.id')),

            Column('number_of_likes', Integer, nullable=False, default=0),
            Column('last_profile_id', Integer)
        )

        self.Navigation = Table(
            'Navigation',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('telegram_id', ForeignKey('Account.telegram_id'), unique=True), 
            Column('menu_id', Enum(constants.MenuIds), nullable=False),
            Column('registration_item_id', Enum(constants.ProfileItemsIds), nullable=False),
            Column('search_parameter_item_id', Enum(constants.SearchParametersItemsIds), nullable=False)
        )

        self.PotentialProfiles = Table(
            'PotentialProfiles',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('telegram_id', ForeignKey('Account.telegram_id')), 
            Column('sender_account_id', Integer, nullable=False),
            Column('requested_account_id', Integer, nullable=False), 
            Column('is_viewed', Boolean, nullable=False, default=False)
        )

        self.SearchParameters = Table(
            'SearchParameters',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('telegram_id', ForeignKey('Account.telegram_id'), unique=True), 
            Column('age', Enum(mp.PreferedAge)),
            Column('spoken_languages', Enum(mp.SpokenLanguages)),
            Column('programming_languages', Enum(mp.ProgrammingLanguages)),
        )

        self.Profile = Table(
            'Profile',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('telegram_id', ForeignKey('Account.telegram_id'), unique=True), 
            Column('first_name', String(255), nullable=False),
            Column('last_name', String(255)),
            Column('age', Integer),
            Column('photo_url', String(255), unique=True),
            Column('spoken_languages', Enum(mp.SpokenLanguages)),
            Column('programming_languages', Enum(mp.ProgrammingLanguages)),
            Column('about_me', String(2000))
        )

        self.metadata.create_all(self.engine)
        self.connection = self.engine.connect()

    def is_registered(self, user_id: int) -> bool:
        result = self.connection.execute(select(self.Account.c['is_registered']).where(self.Account.c['telegram_id'] == user_id))
        return result.mappings().all()[0]['is_registered']

    def register_user(self, user_id: int) -> bool:
        result = self.connection.execute(update(self.Account).where(self.Account.c['telegram_id'] == user_id).values(is_registered=True))

    def get_users_menu_id(self, user_id: int) -> constants.MenuIds:
        result = self.connection.execute(select(self.Navigation.c['menu_id']).where(self.Navigation.c['telegram_id'] == user_id))
        return result.mappings().all()[0]['menu_id']

    def set_users_menu_id(self, user_id: int, new_menu_id: constants.MenuIds) -> None:
        result = self.connection.execute(update(self.Navigation).where(self.Navigation.c['telegram_id'] == user_id).values(menu_id=new_nenu_id))

    def get_users_registration_item_id(self, user_id: int) -> constants.ProfileItemsIds:
        result = self.connection.execute(select(self.Navigation.c['registration_item_id']).where(self.Navigation.c['telegram_id'] == user_id))
        return result.mappings().all()[0]['registration_item_id']

    def set_users_registration_item_id(self, user_id: int, new_registration_item_id: constants.ProfileItemsIds) -> None:
        result = self.connection.execute(update(self.Navigation).where(self.Navigation.c['telegram_id'] == user_id).values(registration_item_id=new_registration_item_id))

    def get_users_profile_item(self, user_id: int, item: constants.ProfileItemsIds) -> Optional[str]:
        pass

    # how to determine what to use: item or value
    def set_users_profile_item(self, user_id: int, item: constants.ProfileItemsIds, value: Optional[str]) -> None:
        pass

    def append_to_users_profile_item(self, user_id: int, item: constants.ProfileItemsIds, value: str) -> None:
        pass

    def are_search_parameters_filled(self, user_id: int) -> bool:
        result = self.connection.execute(select(self.Account.c['are_search_parameters_filled']).where(self.Account.c['telegram_id'] == user_id))
        return result.mappings().all()[0]['are_search_parameters_filled']

    def set_search_parameters_filled(self, user_id: int) -> None:
        result = self.connection.execute(update(self.Account).where(self.Account.c['telegram_id'] == user_id).values(are_search_parameters_filled=True))

    def get_users_search_parameter_item_id(self, user_id: int) -> constants.SearchParametersItemsIds:
        result = self.connection.execute(select(self.Account.c['are_search_parameters_filled']).where(self.Account.c['telegram_id'] == user_id))
        return result.mappings().all()[0]['are_search_parameters_filled']

    def set_users_search_parameter_item_id(self, user_id: int,
                                        new_search_parameter_item_id: constants.SearchParametersItemsIds) -> None:
        result = self.connection.execute(update(self.Navigation).where(self.Navigation.c['telegram_id'] == user_id).values(search_parameter_item_id=item))

    def get_users_search_parameter_item(self, user_id: int, item: constants.SearchParametersItemsIds) -> Optional[str]:
        result = self.connection.execute(select(self.Navigation.c['search_parameter_item_id']).where(self.Navigation.c['telegram_id'] == user_id))
        return result.mappings().all()[0]['search_parameter_item_id']

    def append_to_users_search_parameter_item(self, user_id: int, item: constants.SearchParametersItemsIds,
                                            value: Optional[str]) -> None:
        pass

    def get_users_last_shown_profile_id(self, user_id: int) -> Optional[int]:
        result = self.connection.execute(select(self.Account.c['last_profile_id']).where(self.Account.c['telegram_id'] == user_id))
        return result.mappings().all()[0]['last_profile_id']

    def set_users_last_shown_profile_id(self, user_id: int, candidate_id: int) -> None:
        result = self.connection.execute(update(self.Account).where(self.Account.c['telegram_id'] == user_id).values(last_profile_id=candidate_id))
    
    def get_users_telegram_login_by_id(self, user_id: int) -> str:
        result = self.connection.execute(select(self.Account.c['telegram_login']).where(self.Account.c['telegram_id'] == user_id))
        return result.mappings().all()[0]['telegram_login']

    def get_number_of_likes(self, user_id: int) -> int:
        result = self.connection.execute(select(self.Account.c['number_of_likes']).where(self.Account.c['telegram_id'] == user_id))
        return result.mappings().all()[0]['number_of_likes']

    def inc_number_of_likes(self, user_id: int) -> None:
        result = self.connection.execute(update(self.Account).where(self.Account.c['telegram_id'] == user_id).values(number_of_like = self.get_number_of_likes(user_id) + 1))

DATABASE = DB()

