from typing import Final
from ...tipos import PosicionEnPantalla
from .capa import Capa, CapaIndividual
from .capa_contenedora import CapaContenedora

class CapasAreaDibujo:
    todas: Final[list[Capa]]
    def __init__(self, capa_lienzo: CapaIndividual, capa_dibujo: CapaContenedora, capa_seleccion: CapaIndividual, capa_cursor: CapaIndividual):
        self.capa_lienzo = capa_lienzo
        self.capa_dibujo = capa_dibujo
        self.capa_seleccion = capa_seleccion
        self.capa_cursor = capa_cursor
        self.capa_lienzo.posicion_capa = PosicionEnPantalla((0, 0))
        self.capa_seleccion.posicion_capa = PosicionEnPantalla((0, 0))
        self.todas = [capa_lienzo, capa_dibujo, capa_seleccion, capa_cursor]
