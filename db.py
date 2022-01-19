from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base

import choice_fields as mp # multiple choice

engine = create_engine('sqlite:///testdb.db', echo=True)
Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    telegram_login = Column(String(100), unique=True)

    def __repr__(self):
        return "<Account(id='%s', telegram_login='%s')>" % (self.id, self.telegram_login)

class PotentialProfiles(Base):
    __tablename__ = 'potentialprofiles'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey(Account.id))
    requested_account_id = Column(Integer)
    is_viewed = Column(Boolean)

    def __repr__(self):
        return "<PotentialProfiles(id='%s', account_id='%s', requested_account_id='%s')>" % (self.id, self.account_id, self.requested_account_id)

class SearchParameters(Base):
    __tablename__ = 'searchparameters'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey(Account.id))
    age = Column(Enum(mp.PreferedAge))
    spoken_languages = Column(Enum(mp.SpokenLanguages))
    programming_languages = Column(Enum(mp.ProgrammingLanguages))

    def __repr__(self):
        return "<SearchParameters(id='%s', account_id='%s')>" % (self.id, self.account_id)

class Profile(Base):
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey(Account.id))
    first_name = Column(String(50))
    last_name = Column(String(50))
    age = Column(Integer)
    photo_url = Column(Integer, unique=True)
    spoken_languages = Column(Enum(mp.SpokenLanguages))
    programming_languages = Column(Enum(mp.ProgrammingLanguages))
    about_me = Column(String(1000))

    def __repr__(self):
        return "<Profile(id='%s', account_id='%s')>" % (self.id, self.account_id)

Base.metadata.create_all(engine)
