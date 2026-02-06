from app.database import Base
from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    patronymic = Column(String)
    # login = Column(String, nullable=False)
    time_created: Mapped[datetime] = mapped_column(server_default=func.now())
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=True, unique=True)
    hashed_password: Mapped[str]

