
from typing import Final, Optional, Sequence

from ....dependencias import  PygameRect, CreadorPanelHerramientas,CreadorMuestras, PygameRect
from ...tipos import Tuple2Int, Tuple3Int
from ..surfaces import GenericSurface, GenericSurfaceFactory


class CreadorPanelHerramientasPintaFormas:
    __slots__ = ('creador_panel_herramientas', 'surface_factory')
    creador_panel_herramientas: CreadorPanelHerramientas
    surface_factory: Final[GenericSurfaceFactory]

    def __init__(self, surface_factory: GenericSurfaceFactory) -> None:
        self.surface_factory = surface_factory
        self.creador_panel_herramientas = CreadorPanelHerramientas()

    def crear_surface_herramientas(self,
            imagenes: Sequence[GenericSurface],
            dimensiones: Tuple2Int,
            disposicion: Optional[Tuple2Int] = None,
            ajustes: Optional[dict[str, int]] = None
        ) -> tuple[GenericSurface, list[PygameRect]]:
        imagenes_as_pygame_surfaces = [imagen.get_pygame_surface() for imagen in imagenes]
        surface, rects = self.creador_panel_herramientas.crear_surface_herramientas(
            imagenes_as_pygame_surfaces, dimensiones, disposicion, ajustes
        )
        return (self.surface_factory.from_surface(surface), rects)


class CreadorMuestrasPintaFormas:
    creador_muestras: CreadorMuestras
    surface_factory: Final[GenericSurfaceFactory]

    def __init__(self, surface_factory: GenericSurfaceFactory) -> None:
        self.surface_factory = surface_factory
        self.creador_muestras = CreadorMuestras()

    def crear_surface_muestras(self,
            colores: Sequence[Tuple3Int],
            dimensiones: Tuple2Int,
            disposicion: Optional[Tuple2Int] = None,
            ajustes: Optional[dict[str, int]] = None
        ) -> tuple[GenericSurface, list[PygameRect]]:
        surface, rects = self.creador_muestras.crear_surface_muestras(
            colores, dimensiones, disposicion, ajustes
        )
        return (self.surface_factory.from_surface(surface), rects)
