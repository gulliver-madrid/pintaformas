
from .tuplas import DIMS, TuplaDosEnteros, TuplaTriple, Tuple2Int, Tuple3Int, Tuple4Int
from .convertir_tuplas import convertir_a_tupla_dos_float, convertir_a_tupla_dos_int, convertir_a_tupla_tres_int
from .cev import CodigoElementoVista, codigo_to_string, CodigoForma, CodigoArea, CodigoObjetoEspecial, CodigoStr,CodigoAreaPF



class Posicion(TuplaDosEnteros):
    pass


class PosicionEnPantalla(Posicion):
    pass

class PosicionEnPantallaRelativa(Posicion):
    pass


class PosicionEnDocumento(Posicion):
    pass


class Vector2D(TuplaDosEnteros):
    '''Sirve para describir desplazamientos en el espacio 2D'''


class Desplazamiento(TuplaDosEnteros):
    '''Sirve para describir desplazamientos en el espacio 2D'''


class Dimensiones(TuplaDosEnteros):
    def dividir_por_dimensiones(self, divisor: 'Dimensiones') -> tuple[float, float]:
        return convertir_a_tupla_dos_float(self[dim] / divisor[dim] for dim in DIMS)



class Color(TuplaTriple):
    def __init__(self, tupla: Tuple3Int):
        super().__init__(tupla)
        assert all(0 <= valor <= 255 for valor in tupla)



__all__ = ['CodigoElementoVista', 'CodigoForma', 'CodigoArea', 'CodigoAreaPF', 'CodigoObjetoEspecial', 'CodigoStr', 'codigo_to_string', 'Tuple2Int', 'Tuple3Int', 'Tuple4Int', 'TuplaDosEnteros', 'AutoName', 'convertir_a_tupla_tres_int', 'convertir_a_tupla_dos_int', 'convertir_a_tupla_dos_float']
