from domain.errors.base import DomainError


class NegativePropertyError(DomainError):
    def __init__(self, entity_name: str, property_name: str):
        message = f"Propriedade '{property_name}' de '{entity_name}' não pode ser negativa."
        business_rule = "A grandeza deste valor não pode ser negativo (< 0)."

        super().__init__(message=message, business_rule=business_rule)


class NegativeValueError(DomainError):
    def __init__(self, property_name: str):
        message = f"Valor de '{property_name}' não pode ser negativo."
        business_rule = "A grandeza deste valor não pode ser negativo (< 0)."

        super().__init__(message=message, business_rule=business_rule)