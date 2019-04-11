from typing import Sequence, Optional, List, Tuple, Dict
import pygame
from .colores import GRIS_CLARO, GRIS_OSCURO, NEGRO, TRANSPARENTE_ESPECIAL
from ..compartido import crear_rects

PygameSurface = pygame.surface.Surface
PygameRect = pygame.rect.Rect
Tuple2Int = Tuple[int, int]
X, Y = 0, 1

ESPACIO = 16
LADO_MUESTRA = 80
class CreadorPanelHerramientas:
    def crear_surface_herramientas(self,
            imagenes: Sequence[PygameSurface],
            dimensiones: Tuple2Int,
            disposicion: Optional[Tuple2Int]=None,
            ajustes: Optional[Dict[str, int]]=None) -> Tuple[pygame.Surface, List[PygameRect]]:
        '''No fuerza a que se ocupe todo el espacio del surface'''
        num_imagenes = len(imagenes)
        if disposicion == None:
            disposicion = (num_imagenes, 1)
        assert disposicion is not None
        columnas, filas = disposicion
        num_herramientas = columnas * filas
        imagenes = imagenes[:num_herramientas]
        if ajustes:
            espacio = ajustes['espacio']
            lado_herramienta = ajustes['lado_herramienta']
        else:
            espacio = ESPACIO
            lado_herramienta = LADO_MUESTRA
        return self._crear_surface_herramientas(num_herramientas, dimensiones, imagenes, columnas, filas, lado_herramienta, espacio)


    def _crear_surface_herramientas(self,
            num_herramientas: int,
            dimensiones: Tuple2Int,
            imagenes: Sequence[PygameSurface],
            columnas: int,
            filas: int,
            lado_herramienta: int,
            espacio: int) -> Tuple[pygame.Surface, List[PygameRect]]:

        espacio_horizontal_ocupado = (num_herramientas / filas * lado_herramienta) + (num_herramientas / filas + 1) * espacio
        assert espacio_horizontal_ocupado <= dimensiones[X], f'{espacio_horizontal_ocupado}, {dimensiones[X]}'
        herramientas = pygame.Surface(dimensiones)
        herramientas.fill(GRIS_OSCURO)
        herramientas.set_colorkey(TRANSPARENTE_ESPECIAL)
        pygame.draw.rect(herramientas, GRIS_CLARO, (0, 0, * dimensiones), 5)

        rects_herramientas = crear_rects(len(imagenes), columnas, espacio, lado_herramienta)

        for imagen, rect in  zip(imagenes, rects_herramientas):
            imagen_tamano_correcto = pygame.transform.scale(imagen, rect.size)
            pygame.draw.rect(herramientas, TRANSPARENTE_ESPECIAL, rect)
            herramientas.blit(imagen_tamano_correcto, rect.topleft)
            pygame.draw.rect(herramientas, NEGRO, rect, 3)

        return herramientas, rects_herramientas

class Widget:
    pass
