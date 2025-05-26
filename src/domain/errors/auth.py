# coding utf-8

from ...domain.entities import IError

from ...domain.entities.typing.enums import ErrorCode


class InvalidCredentials(IError):
    """
    Исключение, возникающее при неверных учетных данных.

    Args:
        status_code (int, optional): HTTP статус код ошибки. По умолчанию `ErrorCode.unauthorized`.
        detail (str, optional): Сообщение об ошибке. По умолчанию "Invalid credentials provided".
    """

    def __init__(
        self,
        status_code=ErrorCode.unauthorized,
        detail: str = "Invalid credentials provided",
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail=detail,
        )
