"""
Description of existing models
"""
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """
    The Base class is used as a base for other classes.
    Contains:
        record id
        record creation time
    """
    @declared_attr
    def __tablename__(self):
        return self.__name__

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now, server_default='NOW()')


class User(Base):
    """
    User class for recording all users of the bot.
    Contains:
        tg_id - user id in the telegram
        name - how the bot will refer to the user
    """
    tg_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)


class QuestionAnswer(Base):
    """
    Question-Answer class for recording all questions and answers of the bot.
    Contains:
        question
        answer
    """
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)


class SessionLog(Base):
    """
    Session log class for recording logs of user interaction with the bot.
    Contains:
        user_id - id of the user, who interacts with the bot, from User table
        algorithm - key of the algorithm, that gave answer to the user
        successful - answer evaluation by the user
    """
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    algorithm = Column(String, nullable=False)
    successful = Column(Boolean, nullable=False)


class QuestionAnswerFlag(Base):
    qa_id = Column(Integer, ForeignKey('QuestionAnswer.id'), nullable=False)
    flag = Column(String, nullable=False)


class UserRole(Base):
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    role_title = Column(String, nullable=False)
