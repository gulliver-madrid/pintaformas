from typing import Protocol
from ...dependencias import PygameEvent

class AppProtocol(Protocol):
    def iniciar(self) -> None:
        ...
    def ejecutar_ciclo(self, eventos: list[PygameEvent]) -> None:
        ...

