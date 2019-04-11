from dataclasses import dataclass
from typing import Generic, TypeVar
from .modos import Modos


R = TypeVar('R')

@dataclass
class ComponentesGestoresEventos(Generic[R]):
    realizador: R
    modos: Modos
