
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import relationship

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    donation = relationship('Donation')
