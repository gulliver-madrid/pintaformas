from typing import List, Tuple, Iterable

from pygame.rect import Rect as PygameRect

DIMS = 0, 1


def crear_rects(numero: int, num_columnas: int, espacio: int, lado: int) -> List[PygameRect]:
    '''Crea rects segun la disposicion indicada'''
    dimensiones_rect = (lado, lado)
    rects = []
    for i in range(numero):
        coord = ((i % num_columnas), (i // num_columnas))
        posicion: Tuple[int, int] = crear_posicion(espacio + (espacio + lado) * coord[dim] for dim in DIMS)
        rect = PygameRect(posicion, dimensiones_rect)
        rects.append(rect)
    return rects


def crear_posicion(expresion: Iterable[int]) -> Tuple[int, int]:
    posicion: Tuple[int, int] = tuple(expresion)  # type: ignore [assignment]
    assert len(posicion) == 2
    return posicion
