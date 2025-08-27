from domain.errors.base import DomainError


class EmptyPropertyError(DomainError):
    def __init__(self, entity_name: str, property_name: str):
        message = f"Propriedade '{property_name}' de '{entity_name}' não pode ser vazia."
        business_rule = "Valores obrigatórios não podem ser nulos ou vazios."

        super().__init__(message=message, business_rule=business_rule)


class EmptyValueError(DomainError):
    def __init__(self, property_name: str):
        message = f"Valor de '{property_name}' não pode ser vazio."
        business_rule = "Valores obrigatórios não podem ser nulos ou vazios."

        super().__init__(message=message, business_rule=business_rule)
