from sqlalchemy import create_engine, Column, Date, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_game_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class GameModel(DeclarativeBase):
    """Sqlalchemy game results model"""
    __tablename__ = "gameresults"

    id = Column(Integer, primary_key=True)
    season = Column('season', Integer)
    date = Column('date', Date)
    away = Column('away', String)
    home = Column('home', String)
    away_score = Column('away_score', Integer)
    home_score = Column('home_score', Integer)
    result = Column('result', String)