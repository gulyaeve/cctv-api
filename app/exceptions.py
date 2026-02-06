from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserExistException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже зарегистрирован"


class IncorrectEmailOrPassword(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Некорректный email или пароль"


class TokenMissing(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class TokenIncorrect(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserNotPresent(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь не найден"


class ObjectMissingException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Объект не найден"
