from typing import TYPE_CHECKING, Optional, Protocol, Sequence, Union

from ....dependencias import PygameRect, PygameSurface
from ...tipos import Color, Tuple2Int, Tuple3Int, Tuple4Int
from .wrapper import PygameSurfaceWrapper
from .generic import GenericSurface, RectAmpliado


class SurfaceException(Exception):
    pass



class PygameSurfaceWrapperFactory:
    def from_surface(self, surface: PygameSurface) -> PygameSurfaceWrapper:
        return PygameSurfaceWrapper(surface)

    def from_size(self, size: Tuple2Int) -> PygameSurfaceWrapper:
        return self.from_surface(PygameSurface(size))


class SurfaceObservable:
    blitted: list[tuple['GenericSurface', Tuple2Int]]

    def __init__(self, size: Tuple2Int) -> None:
        self._size = size
        self.blitted = []

    def blit(self, source: GenericSurface, dest: Union[Sequence[float], PygameRect]) -> PygameRect:
        dest_as_tuple: Tuple2Int
        if isinstance(dest, PygameRect):
            dest_as_tuple = dest.x, dest.y
        else:
            dest_as_tuple = int(dest[0]), int(dest[1])
        self.blitted.append((surface, dest_as_tuple))
        return PygameRect(dest_as_tuple, source.get_size())

    def blits(self, blit_sequence: Sequence[tuple[GenericSurface, Tuple2Int]]) -> Optional[list[PygameRect]]:
        raise SurfaceException()


    def fill(self, color: Color, rect: Optional[PygameRect] = None) -> None:
        raise SurfaceException()

    def subsurface(self, rect: PygameRect) -> 'SurfaceObservable':
        raise SurfaceException()

    def get_size(self) -> Tuple2Int:
        raise SurfaceException()

    def set_colorkey(self, color: Tuple3Int) -> None:
        raise SurfaceException()
        ...

    def get_pygame_surface(self) -> PygameSurface:
        raise SurfaceException()
        ...

    def draw_circle(self, tupla_color: Tuple3Int, tupla_posicion: Tuple2Int, radio: int, ancho: int) -> None:
        raise SurfaceException()
        ...

    def draw_line(self, tupla_color: Tuple3Int, tupla_inicio: Tuple2Int, tupla_fin: Tuple2Int, ancho: int) -> None:
        raise SurfaceException()
        ...

    def draw_rect(self, tupla_color: Tuple3Int, rect: RectAmpliado) -> None:
        raise SurfaceException()

    def get_at(self, punto: Tuple2Int) -> Tuple4Int:
        raise SurfaceException()

    def get_rect(self) -> PygameRect:
        raise SurfaceException()
        ...


class SurfaceObservableFactory:
    def from_surface(self, surface: PygameSurface) -> 'SurfaceObservable':
        nuevo = SurfaceObservable((surface.x, surface.y))  # type: ignore [attr-defined]
        return nuevo

    def from_size(self, size: Tuple2Int) -> 'SurfaceObservable':
        return SurfaceObservable(size)


class GenericSurfaceFactory(Protocol):
    def from_surface(self, surface: PygameSurface) -> GenericSurface:
        ...

    def from_size(self, size: Tuple2Int) -> GenericSurface:
        ...

__all__ = ('PygameSurfaceWrapper', 'RectAmpliado', 'GenericSurface')

if TYPE_CHECKING:
    #
    surface_observable: SurfaceObservable
    surface: GenericSurface = surface_observable

    wrapper: PygameSurfaceWrapper
    surface = wrapper

    GenericSurface = GenericSurface

    wrapper_factory: PygameSurfaceWrapperFactory
    generic_factory: GenericSurfaceFactory = wrapper_factory

    surface_observable_factory: SurfaceObservableFactory
    generic_factory = surface_observable_factory
