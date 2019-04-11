from typing import Optional, Protocol, Sequence, Union

from ....dependencias import PygameRect, PygameSurface
from ...tipos import Color, Tuple2Int, Tuple3Int, Tuple4Int

RectAmpliado = Union[PygameRect, Tuple4Int]


class GenericSurface(Protocol):

    def blit(self, source: 'GenericSurface', dest: Union[Sequence[float], PygameRect]) -> PygameRect:
        ...

    def blits(self, blit_sequence: Sequence[tuple['GenericSurface', Tuple2Int]]) -> Optional[list[PygameRect]]:
        ...


    def fill(self, color: Color, rect: Optional[PygameRect] = None) -> None:
        ...

    def subsurface(self, rect: PygameRect) -> 'GenericSurface':
        ...

    def get_size(self) -> Tuple2Int:
        ...

    def set_colorkey(self, color: Tuple3Int) -> None:
        ...

    def get_pygame_surface(self) -> PygameSurface:
        ...

    def draw_circle(self, tupla_color: Tuple3Int, tupla_posicion: Tuple2Int, radio: int, ancho: int) -> None:
        ...

    def draw_line(self, tupla_color: Tuple3Int, tupla_inicio: Tuple2Int, tupla_fin: Tuple2Int, ancho: int) -> None:
        ...

    def draw_rect(self, tupla_color: Tuple3Int, rect: RectAmpliado) -> None:
        ...

    def get_at(self, punto: Tuple2Int) -> Tuple4Int:
        ...

    def get_rect(self) -> PygameRect:
        ...
