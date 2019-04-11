from typing import Union, Optional, cast
import pygame
from ...dependencias import PygameEvent
from ..tipos import PosicionEnPantalla, Vector2D
from ..tipos.transformar import obtener_atributo

StrOrPygameEvent = Union[str, PygameEvent]
DiccInternoPygameEvent = dict[str, object]

class Evento:
    event: Optional[PygameEvent]
    tipo: str
    dicc: Optional[DiccInternoPygameEvent]
    type: Union[str, int]
    def __init__(self, tipo_o_event: StrOrPygameEvent) -> None:
        if isinstance(tipo_o_event, str):
            tipo = tipo_o_event
            self.event = None
            self.type = tipo
            self.tipo = self.type
            self.dicc = None
        else:
            assert isinstance(tipo_o_event, PygameEvent)
            self.event = tipo_o_event
            self.dicc = cast(DiccInternoPygameEvent, self.event.__dict__)
            assert isinstance(self.type, int)
            self.tipo = pygame.event.event_name(self.type)

    def __getattr__(self, nombre: str) -> object:
        return obtener_atributo(self.event, nombre)

    @property
    def posicion(self) -> PosicionEnPantalla:
        assert self.event
        posicion = self.event.pos
        assert isinstance(posicion, tuple), posicion
        return PosicionEnPantalla(posicion)

    @property
    def desplazamiento(self) -> Vector2D:
        assert self.event
        desplazamiento = self.event.rel
        assert isinstance(desplazamiento, tuple)
        return Vector2D(desplazamiento)

    def __repr__(self) -> str:
        # diccionario = cast(Union[dict[str, object], str], self.dicc or '')
        diccionario = self.dicc or ''
        return f'Evento({self.tipo}, {diccionario})'



ACTIVAR = Evento('ACTIVAR')
DESACTIVAR = Evento('DESACTIVAR')
