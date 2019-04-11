from enum import Enum, auto

from ..tipos import PosicionEnPantalla, Color, CodigoElementoVista, CodigoObjetoEspecial
from .. import cfg
from .objeto_modelo import ObjetoModelo

RADIO_CURSOR = 5


class TipoCursor(Enum):
    flecha = auto()
    pintura = auto()


class Cursor(ObjetoModelo):
    __slots__ = (
        'codigo',
        'posicion',
        'color',
        'radio',
        'tipo_cursor',
        '_visibilidad_cursor_so',
        'visibilidad_cursor_manual'
        )
    codigo: CodigoElementoVista
    posicion: PosicionEnPantalla
    color: Color
    radio: int
    tipo_cursor: TipoCursor
    visibilidad_cursor_manual: bool
    _visibilidad_cursor_so: bool

    def __init__(self) -> None:
        self.codigo = CodigoObjetoEspecial.cursor
        self.posicion = PosicionEnPantalla(cfg.POSICION_CURSOR_POR_DEFECTO)
        self.radio = RADIO_CURSOR
        self.tipo_cursor = TipoCursor.flecha
        self.visibilidad_cursor_manual = True
        self.set_visibilidad_cursor_so(False)

    def mover_cursor_a_posicion(self, posicion: PosicionEnPantalla) -> None:
        self.posicion = posicion


    def borra_cursor_manual(self) -> None:
        self.visibilidad_cursor_manual = False

    def muestra_cursor_manual(self) -> None:
        assert not self.visibilidad_cursor_so
        self.visibilidad_cursor_manual = True

    @property
    def visibilidad_cursor_so(self) -> bool:
        return self._visibilidad_cursor_so

    def set_visibilidad_cursor_so(self, valor: bool) -> None:
        self._visibilidad_cursor_so = valor
