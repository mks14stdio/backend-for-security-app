from .settings import settings


class NotFound(Exception):
    detail: str

    def __str__(self):
        return self.detail

    def __init__(self, *, detail) -> None:
        self.detail = f"Не найдено: {detail}"
        if settings.ENV_TYPE == "dev":
            print(f"{self.detail}")


class AuthTokenError(Exception):
    detail: str

    def __str__(self):
        return self.detail

    def __init__(self, original_exception: Exception | None = None) -> None:
        self.detail = "Токен устарел"

        if settings.ENV_TYPE == "dev" and original_exception:
            print(original_exception)


class UserAlreadyExists(Exception):
    detail: str

    def __str__(self):
        return self.detail

    def __init__(self) -> None:
        self.detail = "Пользователь с таким email существует"
