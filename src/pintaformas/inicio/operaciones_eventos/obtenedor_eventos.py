from typing import Protocol
from ...dependencias import PygameEvent

class ObtenedorEventos(Protocol):
    def obtener_eventos(self) -> list[PygameEvent]:
        ...
