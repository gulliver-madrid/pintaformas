
from typing import TYPE_CHECKING
from ...dependencias import get_pygame_events, PygameEvent

class ObtenedorEventosPygame:
    def __init__(self) -> None:
        self.get_pygame_events = get_pygame_events

    def obtener_eventos(self) -> list[PygameEvent]:
        return self.get_pygame_events()

if TYPE_CHECKING:
    from .obtenedor_eventos import ObtenedorEventos
    instancia: ObtenedorEventosPygame
    interfaz: ObtenedorEventos = instancia
