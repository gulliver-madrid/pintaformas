from typing import Final, Optional, Sequence, Union, cast

from ....dependencias import PygameRect, PygameSurface, pygame
from ...tipos import Color, Tuple2Int, Tuple3Int, Tuple4Int
from .generic import GenericSurface, RectAmpliado


class PygameSurfaceWrapper:
    """Envuelve un PygameSurface"""
    _surface: Final[PygameSurface]

    def __init__(self, surface: PygameSurface) -> None:
        self._surface: PygameSurface = surface

    def blit(self, source: GenericSurface, dest: Union[Sequence[float], PygameRect]) -> PygameRect:
        return self._surface.blit(source.get_pygame_surface(), dest)

    def blits(self, blit_sequence: Sequence[tuple[GenericSurface, Tuple2Int]]) -> Optional[list[PygameRect]]:
        pygame_wrapper_seq = cast(Sequence[tuple[PygameSurfaceWrapper, Tuple2Int]], blit_sequence)
        sequence = tuple((surface.get_pygame_surface(), tupla) for surface, tupla in pygame_wrapper_seq)
        return self._surface.blits(blit_sequence=sequence)

    def fill(self, color: Color, rect: Optional[PygameRect] = None) -> None:
        self._surface.fill(color, rect)

    def draw_line(self, tupla_color: Tuple3Int, tupla_inicio: Tuple2Int, tupla_fin: Tuple2Int, ancho: int) -> None:
        pygame.draw.line(self._surface, tupla_color, tupla_inicio, tupla_fin, ancho)

    def subsurface(self, rect: PygameRect) -> 'PygameSurfaceWrapper':
        SelfClass = type(self)
        return SelfClass(self._surface.subsurface(rect))

    def get_size(self) -> Tuple2Int:
        return self._surface.get_size()

    def set_colorkey(self, color: Tuple3Int) -> None:
        self._surface.set_colorkey(color)

    def get_pygame_surface(self) -> PygameSurface:
        return self._surface

    def draw_circle(self, tupla_color: Tuple3Int, tupla_posicion: Tuple2Int, radio: int, ancho: int) -> None:
        pygame.draw.circle(self._surface, tupla_color, tupla_posicion, radio, ancho)

    def draw_rect(self, tupla_color: Tuple3Int, rect: RectAmpliado) -> None:
        pygame.draw.rect(self._surface, tupla_color, rect)

    def get_at(self, punto: Tuple2Int) -> Tuple4Int:
        return self._surface.get_at(punto)

    def get_rect(self) -> PygameRect:
        return self._surface.get_rect()
        ...
