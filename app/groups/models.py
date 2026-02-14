from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped

from app.database import Base


class GroupModel(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)

    schedule: Mapped[List["ScheduleModel"]] = relationship(back_populates="group")
    
    def __str__(self) -> str:
        return f"{self.name}"

