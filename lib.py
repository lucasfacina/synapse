def try_convert(value):
    """
    Tenta converter uma string para int, depois para float.
    Se falhar em ambos, retorna a string original.
    """
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value
