import csv
from io import StringIO
from typing import Iterable, Mapping, Optional


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


def dict_to_csv_line(
        data: Mapping,
        fieldnames: Optional[Iterable[str]] = None,
        delimiter: str = ",",
        newline: bool = True,
) -> str:
    """
    Converte um dicionário numa única linha CSV e garante ordem estável.

    Parâmetros:
      - data: dicionário a ser convertido.
      - fieldnames: sequência de chaves explicitando a ordem desejada. Se fornecida,
        tem precedência e garante ordem estável entre execuções.
      - delimiter: delimitador CSV (padrão ",").
      - newline: se True, inclui '\n' ao final.
    """
    if fieldnames is None:
        # Python 3.7+ preserva ordem de inserção dos dicionários
        fieldnames = list(data.keys())

    output = StringIO()
    writer = csv.writer(output, delimiter=delimiter, lineterminator="\n")
    row = [data.get(k, "") for k in fieldnames]
    writer.writerow(row)
    line = output.getvalue()
    if not newline:
        line = line.rstrip("\n")
    return line


def format_date_to_print(data_aaaammdd):
    """Converte 'AAAAMMDD' para 'DD/MM/AAAA'."""
    if len(data_aaaammdd) == 8:
        ano = data_aaaammdd[0:4]
        mes = data_aaaammdd[4:6]
        dia = data_aaaammdd[6:8]
        return f"{dia}/{mes}/{ano}"
    return data_aaaammdd


def format_date_to_save(data_ddmmaaaa):
    """Converte 'DD/MM/AAAA' para 'AAAAMMDD'."""
    try:
        dia, mes, ano = data_ddmmaaaa.split('/')
        if len(dia) == 2 and len(mes) == 2 and len(ano) == 4:
            return ano + mes + dia
    except:
        return None
