from typing import TYPE_CHECKING, Optional, Protocol

from ..tipos import CodigoElementoVista, Dimensiones
from .capas.capa import Capa
from .surfaces.generic import GenericSurface


class ObjetoConCapasInternas(Protocol):
    capas_internas: list[Capa]
    surface: Optional[GenericSurface]
    dimensiones: Dimensiones

    def reestablecer_fondo(self) -> None:
        ...

    @property
    def codigo(self) -> CodigoElementoVista:
        ...


if TYPE_CHECKING:
    from .areas.area_dibujo import AreaDibujo
    from .capas.capa_contenedora import CapaContenedora

    area_dibujo: AreaDibujo
    objeto_capas_internas: ObjetoConCapasInternas = area_dibujo

    contenedora: CapaContenedora
    objeto_capas_internas = contenedora
