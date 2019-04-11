from typing import ClassVar, Final, Optional

from ...tipos import Color, Tuple3Int, CodigoElementoVista, PosicionEnPantalla
from ..objeto_con_surface import ObjetoConSurface
from ... import cfg

POSICION_CAPA_POR_DEFECTO = PosicionEnPantalla((0, 0))


class Capa(ObjetoConSurface):
    __slots__ = ('color_fondo', 'posicion_capa')

    tipo_de_capa: ClassVar[str]
    posicion_capa: PosicionEnPantalla
    color_fondo: Final[Color]

    def __init__(self, codigo: CodigoElementoVista):
        self.surface = None
        self.color_fondo = Color(cfg.COLOR_TRANSPARENTE)
        self._codigo = codigo
        self.posicion_capa = POSICION_CAPA_POR_DEFECTO

    def reestablecer_fondo(self) -> None:
        assert self.surface
        self.surface.set_colorkey(self.color_fondo)
        self.surface.fill(self.color_fondo)



class CapaIndividual(Capa):
    __slots__ = ('nombre')
    nombre: Optional[str]

    tipo_de_capa = 'individual'

    def __init__(self, codigo: CodigoElementoVista, nombre: Optional[str] = None):
        self.nombre = nombre
        super().__init__(codigo)
