from sqlalchemy import Column, String, Text

from app.core.db import Base

from .base import PreClass


class CharityProject(Base, PreClass):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
