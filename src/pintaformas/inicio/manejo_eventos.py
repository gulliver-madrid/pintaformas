from typing import Final, Optional

from ..dependencias import PygameEvent
from ..core.ajustes_generales import AjustesGenerales
from .operaciones_eventos import ListaTotalDeEventos, PostprocesadorEventos

# TYPE_CHECKING
from .operaciones_eventos import ObtenedorEventos

class ManejoEventos:
    """Agrupa y gestiona los componentes del programa relacionados con los eventos a nivel de programa"""
    obtenedor_eventos: Final[ObtenedorEventos]
    postprocesador_eventos: Optional[PostprocesadorEventos]
    eventos_guardados: Optional[ListaTotalDeEventos]
    ajustes: Final[AjustesGenerales]

    def __init__(self, obtenedor_eventos: ObtenedorEventos,
            ajustes: AjustesGenerales) -> None:
        self.ajustes = ajustes
        self.obtenedor_eventos = obtenedor_eventos

        if self.ajustes['grabar_eventos']:
            self.eventos_guardados = []
            self.postprocesador_eventos = PostprocesadorEventos(self.eventos_guardados)
        else:
            self.eventos_guardados = None
            self.postprocesador_eventos = None

    def obtener_eventos(self) -> list[PygameEvent]:
        eventos = self.obtenedor_eventos.obtener_eventos()
        if self.ajustes['grabar_eventos']:
            assert self.eventos_guardados is not None
            self.eventos_guardados.append(eventos.copy())
        return eventos
