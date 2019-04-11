from typing import Sequence, Tuple, Optional, List, Dict, Union
import pygame
from pygame.rect import Rect as PygameRect
from .colores import GRIS_CLARO, GRIS_OSCURO, NEGRO
from ..compartido import crear_rects

X, Y = 0, 1
ESPACIO = 16
LADO_MUESTRA = 80
class CreadorMuestras:
    def crear_surface_muestras(self,
            colores: Sequence[Tuple[int, int, int]],
            dimensiones: Tuple[int, int],
            disposicion: Optional[Tuple[int, int]] = None,
            ajustes: Optional[Dict[str, int]] = None
            )-> Tuple[pygame.Surface, List[PygameRect]]:
        '''No fuerza a que se ocupe todo el espacio del surface'''
        num_colores = len(colores)
        if disposicion == None:
            disposicion = (num_colores, 1)
        assert disposicion
        columnas, filas = disposicion
        num_muestras = columnas * filas
        colores = colores[:num_muestras]
        if ajustes:
            espacio = ajustes['espacio']
            lado_muestra = ajustes['lado_muestra']
        else:
            espacio = ESPACIO
            lado_muestra = LADO_MUESTRA
        muestras, rects_colores = self._crear_surface_muestras(num_muestras, dimensiones, colores, columnas, filas, lado_muestra, espacio)
        return muestras, rects_colores


    def _crear_surface_muestras(self,
            num_muestras: int,
            dimensiones: Tuple[int, int],
            colores: Sequence[Tuple[int, int, int]],
            columnas: int,
            filas: int,
            lado_muestra: int,
            espacio: int
            ) -> Tuple[pygame.Surface, List[PygameRect]]:

        espacio_horizontal_ocupado = (num_muestras / filas * lado_muestra) + (num_muestras / filas + 1) * espacio
        assert espacio_horizontal_ocupado <= dimensiones[X], f'{espacio_horizontal_ocupado}, {dimensiones[X]}'
        muestras = pygame.Surface(dimensiones)
        muestras.fill(GRIS_OSCURO)
        pygame.draw.rect(muestras, GRIS_CLARO, (0, 0, *dimensiones), 5)

        rects_colores = crear_rects(len(colores), columnas, espacio, lado_muestra)

        for color, rect in zip(colores, rects_colores):
            dibujar_rectangulo(muestras, color, rect, 0)
            dibujar_rectangulo(muestras, NEGRO, rect, 3)

        return muestras, rects_colores



class Widget:
    pass



Tuple3Int = Tuple[int, int, int]
Tuple4Int = Tuple[int, int, int, int]
RectAmpliado = Union[PygameRect, Tuple4Int]

def dibujar_rectangulo(surface: pygame.Surface, color: Tuple3Int, rect: RectAmpliado, ancho: int) -> None:
    args = surface, color, rect, ancho
    try:
        pygame.draw.rect(surface, color, rect, ancho)
    except TypeError as error:
        raise TypeError(f'Argumentos: {args}') from error
