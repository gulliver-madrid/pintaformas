from dataclasses import dataclass
from typing import Final

from ...dependencias import PygameEvent, nombres_pygame
from .nombres import obtener_nombre_tecla
from .excepciones_eventos import EventoUsado
from .evento import Evento
from .modos import Modos

TECLAS_CONTROL = ('left ctrl', 'right ctrl')
TECLAS_SHIFT = ('left shift', 'right shift')
TECLAS_MODALES = TECLAS_CONTROL + TECLAS_SHIFT

@dataclass
class AccionSobreTeclas:
    nombre: str
    valor_modo: bool

ACCIONES_SOBRE_TECLAS = {
    nombres_pygame.KEYDOWN: AccionSobreTeclas('pulsar', True),
    nombres_pygame.KEYUP: AccionSobreTeclas('soltar', False)
}


class GestorDeEventosBase:
    _modos: Final[Modos]
    _ultimos_eventos: Final[list[PygameEvent]]
    def __init__(self, modos: Modos):
        self._modos = modos
        self._ultimos_eventos = []

    def incorporar_eventos(self, eventos: list[PygameEvent]) -> None:
        self._ultimos_eventos.clear()
        self._ultimos_eventos.extend(eventos)

    def procesar_eventos(self) -> None:
        ...

    def procesar_cambio_de_modo(self, evento: Evento) -> None:
        '''
        Procesa un posible cambio de modo.
        Eleva una excepcion EventoUsado si se produce el cambio.
        '''

        if not evento.type in ACCIONES_SOBRE_TECLAS:
            return
        assert isinstance(evento.type, int)
        nombre_tecla = obtener_nombre_tecla(evento)
        if nombre_tecla in TECLAS_MODALES:
            accion = ACCIONES_SOBRE_TECLAS[evento.type]
            valor_modo = accion.valor_modo
            assert isinstance(valor_modo, bool)
            # print(accion.nombre, nombre_tecla)

            if nombre_tecla in TECLAS_CONTROL:
                self._modos.establecer('control', valor_modo)
            else:
                assert nombre_tecla in TECLAS_SHIFT
                self._modos.establecer('shift', valor_modo)
            raise EventoUsado
