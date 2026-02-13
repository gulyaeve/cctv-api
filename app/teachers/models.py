from sqlalchemy import Column, Integer, String

from app.database import Base


class TeacherModel(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    
    def __str__(self) -> str:
        return f"{self.name}"

