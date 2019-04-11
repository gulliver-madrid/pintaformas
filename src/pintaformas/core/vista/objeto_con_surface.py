from typing import Optional

from ...core.vista.surfaces import GenericSurface
from ..tipos.cev import CodigoElementoVista
from ..objetos import Objeto


class ObjetoConSurface(Objeto):
    __slots__ = ('surface', '_codigo')

    _codigo: CodigoElementoVista
    surface: Optional[GenericSurface]

    @property
    def codigo(self) -> CodigoElementoVista:
        return self._codigo
