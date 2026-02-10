from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)


role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permisson_id", Integer, ForeignKey("permissions.id"), primary_key=True),
)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    full_name = Column(String)
    email = Column(String, nullable=False, unique=True)
    # phone = Column(String, nullable=True, unique=True)
    hashed_password = Column(String)
    time_created: Mapped[datetime] = mapped_column(server_default=func.now())
    last_login = Column(DateTime, nullable=True, default=None)

    roles = relationship("Role", secondary=user_roles, back_populates="users")

    def __str__(self) -> str:
        return f"{self.username}"


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    permissions = relationship(
        "Permission", secondary=role_permissions, back_populates="roles"
    )
    users = relationship("UserModel", secondary=user_roles, back_populates="roles")

    def __str__(self) -> str:
        return f"{self.name}"


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    roles = relationship(
        "Role", secondary=role_permissions, back_populates="permissions"
    )

    def __str__(self) -> str:
        return f"{self.name}"
