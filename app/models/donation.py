from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base

from .base import PreClass


class Donation(Base, PreClass):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
