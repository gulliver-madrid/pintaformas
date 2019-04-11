from dataclasses import dataclass, field
from typing import Generic, TypeVar

from ..modos import Modos
from ..evento import Evento
from ..componentes import ComponentesGestoresEventos

from typing_extensions import Protocol


class MetodoInit(Protocol):
    def __call__(self) -> None:
        ...

R = TypeVar('R')

@dataclass
class GestorDeEventosEspecifico(Generic[R]):
    '''Clase abstracta para los diferentes gestores de eventos especificos'''

    _componentes: ComponentesGestoresEventos[R]
    realizador: R = field(init=False)
    _modos: Modos = field(init=False)
    init: MetodoInit = field(init=False)

    def __post_init__(self) -> None:
        self.realizador = self._componentes.realizador
        self._modos = self._componentes.modos
        self.init() # TODO: renombrar a _init


    def procesar_evento(self, evento: Evento) -> None:
        pass
