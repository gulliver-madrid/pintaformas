from typing import Union, overload, TypeVar
from ...tipos import Tuple2Int, TuplaDosEnteros, convertir_a_tupla_dos_int, Posicion
DIMS = 0, 1

ValorEscalable = Union[int, Tuple2Int]

T = TypeVar('T', int, Tuple2Int, TuplaDosEnteros, Posicion)


class Escalado:
    '''Instrumento de ayuda para calcular longitudes a partir de una unidad
    de longitud determinada'''
    def __init__(self, unidad: float):
        self.unidad = unidad
    # @overload
    # def __call__(self, valor: int) -> int:
    #     ...
    #
    # @overload
    # def __call__(self, valor: TuplaDosEnteros) -> TuplaDosEnteros:
    #     ...
    #
    # @overload
    # def __call__(self, valor: T) -> T:
    #     ...


    def __call__(self, valor: T) -> T:
        if isinstance(valor, int):
            return round(valor * self.unidad)
        elif isinstance(valor, TuplaDosEnteros):
            return valor.__class__(self(valor[dim]) for dim in DIMS)
        elif isinstance(valor, tuple):
            return convertir_a_tupla_dos_int(self(valor[dim]) for dim in DIMS)
        else:
            raise ValueError()
