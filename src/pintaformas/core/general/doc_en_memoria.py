import collections
from typing import Iterator

from ..elementos.forma import Forma

UserListForma = collections.UserList[Forma]


class DocumentoEnMemoria(UserListForma):
    '''
    Conserva el historial de comandos
    '''
    data: list[Forma]
    def append(self, elemento: Forma) -> None:
        num_comandos = len(self)
        if num_comandos and num_comandos % 2000 == 0:
            print(f"ATENCION: el documento tiene ya {num_comandos} comandos registrados")
            input('Pulsa ENTER para seguir')
        self.data.append(elemento)

    def pop(self, *args: int) -> Forma:
        return self.data.pop(*args)

    def __iter__(self) -> Iterator[Forma]:
        return iter(self.data)
