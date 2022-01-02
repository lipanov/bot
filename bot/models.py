import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    ForeignKey,
    Boolean,
    DateTime
)
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now, server_default='NOW()')


class User(Base):
    tg_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)

