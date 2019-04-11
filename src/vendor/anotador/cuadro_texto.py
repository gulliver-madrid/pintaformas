from typing import Optional
from .dependencias import pygame
from . import cfg
from .tipos import Tuple2Int, Tuple3Int

POSICION_INICIAL = (20, 20)
class CuadroDeTexto(pygame.surface.Surface):
    def __init__(self,
            surfaceTexto: pygame.surface.Surface,
            fondo: Tuple3Int,
            *,
            ancho_minimo: Optional[int] = None,
            # Lo que sigue se anadio para poder eliminar margenes
            posicion: Optional[Tuple2Int] = None,
            margen_extra: Optional[Tuple2Int] = None,
    ):
        '''
        Crea el cuadro de texto añadiendo margenes al surfaceTexto.
        '''
        self.surfaceTexto = surfaceTexto
        if margen_extra:
            self.ancho_extra = margen_extra[0]
            self.alto_extra = margen_extra[1]
        else:
            self.ancho_extra = cfg.MARGEN_TEXTO * 2
            self.alto_extra = cfg.MARGEN_TEXTO * 2
        if not ancho_minimo:
            ancho_minimo = 0
        self.ancho_minimo = ancho_minimo
        ancho, alto = self._obtener_dimensiones()
        super().__init__((ancho, alto))
        # self.fill(fondo) # Esto seria si queremos tener un fondo uniforme
        if not posicion:
            posicion = POSICION_INICIAL
        assert posicion
        self.blit(surfaceTexto, posicion)


    def _obtener_dimensiones(self) -> Tuple2Int:
        ancho_texto, alto_texto = self.surfaceTexto.get_size()
        ancho_recuadro = self._obtener_ancho_recuadro(ancho_texto)
        alto_recuadro = alto_texto + self.alto_extra
        return ancho_recuadro, alto_recuadro


    def _obtener_ancho_recuadro(self, ancho_texto: int) -> int:
        '''Añade margen al ancho del cuadro de texto y garantiza un minimo'''
        ancho_recuadro = ancho_texto + self.ancho_extra
        ancho_recuadro = max(ancho_recuadro, self.ancho_minimo)
        return ancho_recuadro
