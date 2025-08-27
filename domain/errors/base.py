from shared.error import BaseError


class DomainError(BaseError):
    """
    Representa um erro de violação de uma regra de negócio ou invariante do domínio.
    Esses erros são sempre operacionais, pois resultam de uma tentativa de
    colocar o domínio em um estado inválido. A causa é sempre uma string
    que descreve a regra de negócio quebrada.
    """

    def __init__(self, message: str, business_rule: str):
        # A causa é a regra de negócio e é sempre operacional.
        super().__init__(message=message, cause=business_rule, is_operational=True)
        self.business_rule = business_rule