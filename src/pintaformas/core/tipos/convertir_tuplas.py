from typing import  Union,  Iterable

from .tuplas import  Tuple2Int, Tuple3Int


def convertir_a_tupla_tres_int(expresion: Iterable[int]) -> Tuple3Int:
    '''Cambia el tipo de un objeto perteneciente a una clase derivada de TuplaTriple
    a TuplaTriple.'''
    x: int
    y: int
    z: int
    tupla = tuple(expresion)
    assert len(tupla) == 3
    x, y, z = tupla
    return (x, y, z)


def convertir_a_tupla_dos_int(expresion: Union[Iterable[int], Tuple2Int]) -> Tuple2Int:
    x: int
    y: int
    tupla = tuple(expresion)
    assert len(tupla) == 2
    x, y = tupla
    return (x, y)


def convertir_a_tupla_dos_float(expresion: Union[Iterable[float], tuple[float, float]]) -> tuple[float, float]:
    x: float
    y: float
    tupla = tuple(expresion)
    assert len(tupla) == 2
    x, y = tupla
    return (x, y)
