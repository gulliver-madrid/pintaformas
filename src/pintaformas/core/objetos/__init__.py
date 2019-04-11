
from ..tipos.cev import CodigoElementoVista
from .mas_objetos import DIMS
from .objeto import Objeto


class ObjetoVectorial:
    __slots__ = ('codigo')
    codigo: CodigoElementoVista

__all__ = ['Objeto', 'DIMS']
