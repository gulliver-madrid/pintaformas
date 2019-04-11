from typing import Type, TypeVar, Union
from ....dependencias import nombres_pygame
from ....log_pintaformas import log
from ..evento import Evento
from .especifico import GestorDeEventosEspecifico
from .teclado import GestorEventosTecladoBase

R = TypeVar('R')

class GestorDeEventosGeneral(GestorDeEventosEspecifico[R]):
    '''Clase abstracta para los gestores de eventos generales'''
    clase_gestor_teclado: Type[GestorEventosTecladoBase[R]]
    gestor_teclado: GestorEventosTecladoBase[R]

    def init(self) -> None:
        self.gestor_teclado = self.clase_gestor_teclado(self._componentes)

    def procesar_evento(self, evento: Evento) -> None:
        with log.log_multinivel.abrir_autocierre(
            'procesar_evento', f'{type(self).__name__} procesa el evento {evento.tipo} {evento.dicc}'
        ):
            tipo_evento = evento.type
            if tipo_evento == nombres_pygame.MOUSEMOTION:
                self.evaluar_movimiento_raton(evento)
            elif self.gestor_teclado.es_pulsacion_tecla(evento):
                self.gestor_teclado.procesar_evento(evento)
            else:
                self.evaluar_otros_eventos(evento, tipo_evento)


    def evaluar_movimiento_raton(self, evento: Evento) -> None:
        pass

    def evaluar_otros_eventos(self, evento: Evento, tipo_evento: Union[str, int]) -> None:
        pass
