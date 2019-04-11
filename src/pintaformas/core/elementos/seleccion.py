from typing import Optional

from ..tipos import CodigoObjetoEspecial
from ..objetos import ObjetoVectorial
from .objeto_modelo import ObjetoModelo


class Seleccion(ObjetoModelo):
    __slots__ = ('objeto_seleccionado', 'codigo', 'indice_capa_seleccionada')
    codigo: CodigoObjetoEspecial
    objeto_seleccionado: Optional[ObjetoVectorial]
    indice_capa_seleccionada: Optional[int]

    def __init__(self) -> None:
        self.codigo = CodigoObjetoEspecial.seleccion
        self.objeto_seleccionado = None
        self.indice_capa_seleccionada = None
