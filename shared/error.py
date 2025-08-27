from typing import Optional, Union


class BaseError(Exception):
    """
    Qualquer erro que não herde desta classe é considerado
    um erro inesperado (um bug ou falha não prevista).
    """

    def __init__(
            self,
            message: str,
            cause: Optional[Union[Exception, str]] = None,
            is_operational: bool = True
    ):
        super().__init__(message)
        self.message = message
        self.cause = cause
        self.is_operational = is_operational  # Indica se o erro é esperado (operacional) ou não (bug)

    def __str(self):
        if self.cause:
            return f"{self.message} (Causa: {self.cause})"
        return self.message

    def __repr__(self):
        return f"{self.__class__.__name__}(message='{self.message}', cause={repr(self.cause)})"

