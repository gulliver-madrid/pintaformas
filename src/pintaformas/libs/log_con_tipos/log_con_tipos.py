from typing import Optional

from .categorias import Categoria
from .dependencias_log import LogMultinivel



class LogConTipos:
    __slots__ = ('log_multinivel')
    log_multinivel: LogMultinivel

    def __init__(self) -> None:
        self.log_multinivel = LogMultinivel()

    def abrir(self, categoria: Categoria, mensaje: str) -> None:
        self.log_multinivel.abrir(categoria, mensaje)

    def cerrar(self, categoria: Optional[Categoria] = None, mensaje: Optional[str] = None) -> None:
        self.log_multinivel.cerrar(categoria, mensaje)

    def imprimir_logs(self) -> None:
        self.log_multinivel.imprimir_logs()

    def anotar(self, mensaje: str, categoria: Optional[Categoria] = None) -> None:
        self.log_multinivel.anotar(mensaje, categoria)

    @property
    def nivel_actual(self) -> int:
        return self.log_multinivel.nivel_actual
