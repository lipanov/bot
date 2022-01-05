"""
Description of existing models
"""
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
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
