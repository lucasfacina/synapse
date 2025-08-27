from enum import Enum, auto
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


class Status(Enum):
    ENABLED = auto()
    JUNK = auto()


@dataclass
class File:
    id: str = field(default_factory=lambda: str(uuid.uuid4()), kw_only=True)
    status: Status = field(default=Status.ENABLED, kw_only=True)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc), kw_only=True)
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc), kw_only=True)

    def __setattr__(self, name, value):
        """
        Sobrescreve o metodo de atribuição de atributos.
        Este metodo é chamado TODA vez que um atributo recebe um valor.
        """
        # 1. Primeiro, executa a atribuição normal do atributo.
        #    Usamos `object.__setattr__` para evitar um loop de recursão infinita,
        #    pois chamar `self.nome = valor` aqui dentro chamaria o __setattr__ novamente.
        object.__setattr__(self, name, value)

        # 2. Depois, verificamos se a alteração não foi no próprio 'updated_at'
        #    e se o atributo 'updated_at' de fato já existe no objeto.
        #    (A segunda verificação evita erros durante a inicialização do objeto).
        if name != 'updated_at' and hasattr(self, 'updated_at'):
            # 3. Se a condição for verdadeira, atualizamos o 'updated_at' para o tempo atual.
            #    Usamos `object.__setattr__` novamente para evitar a recursão.
            object.__setattr__(self, 'updated_at', datetime.now(timezone.utc))
