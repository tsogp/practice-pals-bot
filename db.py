from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

import choice_fields as mp # multiple choice

class DB():
    def __init__(self):
        self.metadata = MetaData()
        self.engine = create_engine('sqlite:///testdb.db', echo=True)

        self.account = Table(
            'Account',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('telegram_login', String(255), unique=True, nullable=False)
        )

        self.potentialprofiles = Table(
            'PotentialProfiles',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('account_id', Integer, ForeignKey('Account.id')),
            Column('requested_account_id', Integer, nullable=False), 
            Column('is_viewed', Boolean, nullable=False)
        )

        self.searchparameters = Table(
            'SearchParameters',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('account_id', Integer, ForeignKey('Account.id'), nullable=False),
            Column('age', Enum(mp.PreferedAge)),
            Column('spoken_languages', Enum(mp.SpokenLanguages)),
            Column('programming_languages', Enum(mp.ProgrammingLanguages)),
        )

        self.profile = Table(
            'Profile',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('account_id', Integer, ForeignKey('Account.id'), nullable=False),
            Column('first_name', String(255), nullable=False),
            Column('last_name', String(255)),
            Column('age', Integer),
            Column('photo_url', String(255), unique=True),
            Column('spoken_languages', Enum(mp.SpokenLanguages)),
            Column('programming_languages', Enum(mp.ProgrammingLanguages)),
            Column('about_me', String(2000))
        )

        self.metadata.create_all(self.engine)

DATABASE = DB()

