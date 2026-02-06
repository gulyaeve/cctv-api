from sqladmin import ModelView

from app.users.models import UserModel


class UsersAdmin(ModelView, model=UserModel):
    can_create = False
    can_delete = True
    name = "Пользователь"
    name_plural = "Пользователи"
    column_list = [
        UserModel.id,
        UserModel.name,
        UserModel.surname,
        UserModel.patronymic,
        UserModel.email,
        UserModel.phone,
    ]
    column_details_exclude_list = [UserModel.hashed_password]
