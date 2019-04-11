from typing import ClassVar, Final, Iterator, Union

from ..tipos.cev import CodigoForma
from ..tipos.transformar import obtener_atributo, iterar_sobre_items_atributos
from ..objetos import ObjetoVectorial


class Forma(ObjetoVectorial):
    '''Clase base para todas las formas dibujables en un documento'''
    __slots__ = ()
    tipo: ClassVar[str]
    num_forma: ClassVar[int] = 0
    atributos_eq: ClassVar[list[str]] = []

    def __init__(self) -> None:
        Forma.num_forma += 1
        self.codigo = CodigoForma(
            f'forma_{str(self.num_forma).zfill(4)}'
        )

    def __repr__(self) -> str:
        atributos: list[str] = []
        atributos_items = iterar_sobre_items_atributos(self)
        for nombre, valor in atributos_items:
            atributos.append(f'{nombre}={valor}')
        class_name = type(self).__name__
        atributos_str = ', '.join(atributos)
        return f"{class_name}({atributos_str})"

    def __eq__(self, otro: object) -> bool:
        return type(self) == type(otro) and all(
            obtener_atributo(self, nombre) == obtener_atributo(otro, nombre)
            for nombre in self.atributos_eq
        )
