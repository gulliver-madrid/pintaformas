from ....dependencias import PygameRect
from ...tipos.cev import CodigoArea
from ..surfaces import GenericSurface
from ..objeto_con_surface import ObjetoConSurface
from ...tipos import Dimensiones, Posicion, Color


class Area(ObjetoConSurface):
    __slots__ = ('rect', 'posicion', 'dimensiones')
    _codigo: CodigoArea
    rect: PygameRect
    posicion: Posicion
    dimensiones: Dimensiones

    def set_rect(self, rect: PygameRect) -> None:
        self.rect = rect
        self.posicion = Posicion(rect.topleft)
        self.dimensiones = Dimensiones(rect.size)


class AreaAutoactualizable(Area):
    '''Area que tiene el metodo actualizar_vista'''
    __slots__ = ('fondo',)

    fondo: Color

    def set_surface(self, surface: GenericSurface) -> None:
        assert not self.surface
        self.surface=surface

    def _rellenar_fondo(self) -> None:
        assert self.surface
        self.surface.fill(self.fondo)

    def actualizar_vista(self) -> None:
        """Debe implementarse en las subclases"""
        pass
