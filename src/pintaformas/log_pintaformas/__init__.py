from .categorias import cat
from .ajuste_log import GestorLogPintaFormas
from .dependencias_log import LogConTipos


log = LogConTipos()

__all__ = ['log', 'cat', 'GestorLogPintaFormas']
