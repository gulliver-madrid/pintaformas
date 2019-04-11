from typing import Literal, Optional, Union


from ...log_pintaformas import log, cat
from ...core import cfg
from ..elementos.herramienta import Herramienta
from ..control_general.realizador import Realizador
from .universal.general import GestorDeEventosUniversal
from .bases.general import GestorDeEventosGeneral
from .excepciones_eventos import EventoUsado
from .evento import DESACTIVAR, ACTIVAR, Evento
from .gestor_eventos_base import GestorDeEventosBase
from .modos import Modos

# TYPE_CHECKING
from ..general.observador_herramienta import EstadoHerramientaObservado



KeyGestorEventos = Union[Herramienta, Literal['universal']]


class GestorDeEventos(GestorDeEventosBase):
    herramienta_anterior: Optional[Herramienta]

    def __init__(self, realizador: Realizador,
            modos: Modos,
            gestores_eventos_generales: dict[KeyGestorEventos, GestorDeEventosGeneral[Realizador]],
            estado_herramienta_observado: EstadoHerramientaObservado):
        self.realizador = realizador
        self.estado_herramienta_observado = estado_herramienta_observado
        self.gestores_eventos_generales = gestores_eventos_generales
        universal = self.gestores_eventos_generales['universal']
        assert isinstance(universal, GestorDeEventosUniversal)
        self.gestor_eventos_universal = universal
        self.herramienta_anterior = None
        super().__init__(modos)


    def procesar_eventos(self) -> None:
        """
        Los eventos son procesados en primer lugar por el gestor de eventos universal, y si este no los usa entonces seran procesados por el gestor de eventos en foco.
        """
        eventos = self._ultimos_eventos[:]
        seguir = True
        while seguir:
            if self.estado_herramienta_observado.valor != self.herramienta_anterior:
                self._procesar_cambio_de_herramienta()

            elif eventos:
                log.anotar(f"Quedan {len(eventos)} eventos por procesar", cat.eventos.procesar_eventos)
                evento_puro = eventos.pop(0)
                log.anotar(f"{evento_puro=}", cat.eventos.todos_los_eventos)
                # if 'window' in evento_puro.__dict__.keys():
                #     del evento_puro.__dict__['window']
                evento = Evento(evento_puro)
                try:
                    self.procesar_cambio_de_modo(evento)
                    self.gestor_eventos_universal.procesar_evento(evento)
                    self.gestor_eventos_en_foco.procesar_evento(evento)
                except EventoUsado:
                    continue

            else:
                seguir = False

    def _procesar_cambio_de_herramienta(self) -> None:
        if self.herramienta_anterior:
            gestor_anterior = self.gestores_eventos_generales[self.herramienta_anterior]
            gestor_anterior.procesar_evento(DESACTIVAR)
        self.herramienta_anterior = self.estado_herramienta_observado.valor

        self.gestor_eventos_en_foco.procesar_evento(ACTIVAR)


    @property
    def gestor_eventos_en_foco(self) -> GestorDeEventosGeneral[Realizador]:
        herramienta_actual = self.estado_herramienta_observado.valor
        return self.gestores_eventos_generales[herramienta_actual]
