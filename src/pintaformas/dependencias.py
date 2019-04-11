from ..vendor.anotador.api import Anotador
from typing import TYPE_CHECKING
from ..vendor.componentes_pygame.muestras.api import CreadorMuestras
from ..vendor.componentes_pygame.herramientas.api import CreadorPanelHerramientas
import appdirs  # type: ignore [import]
from pygame import locals as _nombres_pygame
import pygame


ESTE_PAQUETE = 'Proyectos.PintaFormas'





class NombresPygame:
    # TODO: Cambiar nombre a ConstantesPygame

    def __init__(self, _nombres_pygame: object) -> None:
        self._nombres_pygame = _nombres_pygame

    def __getattr__(self, nombre: str) -> int:
        valor: int = getattr(self._nombres_pygame, nombre)
        assert isinstance(valor, int)
        return valor


nombres_pygame = NombresPygame(_nombres_pygame)


crear_evento_pygame = pygame.event.Event
if TYPE_CHECKING:
    PygameEvent = pygame.event.Event
else:
    PygameEvent = pygame.event.EventType
PygameClock = pygame.time.Clock
get_pygame_events = pygame.event.get

PygameSurface = pygame.surface.Surface
PygameRect = pygame.rect.Rect

__all__ = ['appdirs', 'pygame', 'CreadorMuestras', 'CreadorPanelHerramientas', 'Anotador', ]
