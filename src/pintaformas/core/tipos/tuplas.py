from typing import Iterable, TypeVar

Tuple2Int = tuple[int, int]
Tuple3Int = tuple[int, int, int]
Tuple4Int = tuple[int, int, int, int]


DIMS = 0, 1


T = TypeVar('T', bound='TuplaDosEnteros')

class TuplaDosEnteros(Tuple2Int):
    def __init__(self, _ya_usado: Iterable[int]) -> None:
        tupla = tuple(self)
        if len(tupla) != 2 or not all(isinstance(valor, int) for valor in tupla):
            raise ValueError(f'{tupla} no es un valor valido para iniciar TuplaDosEnteros')


    def _suma_vectorial(self: T, otro: Tuple2Int, signo: int = 1) -> T:
        assert signo in (-1, 1)
        assert isinstance(otro, tuple)
        assert len(otro) == 2
        return self.__class__(self[dim] + signo * otro[dim] for dim in DIMS)

    def sumar(self: T, otro: Tuple2Int) -> T:
        return self._suma_vectorial(otro)

    def restar(self: T, otro: Tuple2Int) -> T:
        return self._suma_vectorial(otro, -1)

    def sumar_entero(self: T, entero: int) -> T:
        return self._suma_vectorial((entero, entero))

    def restar_entero(self: T, entero: int) -> T:
        return self._suma_vectorial((entero, entero), -1)

    def __abs__(self: T) -> T:
        return self.__class__(abs(self[dim]) for dim in DIMS)



class TuplaTriple(Tuple3Int):
    '''Tupla con tres elementos que deben ser enteros'''

    def __init__(self, tupla: Tuple3Int):
        assert len(tupla) == 3
        assert all(isinstance(valor, int) for valor in tupla)
