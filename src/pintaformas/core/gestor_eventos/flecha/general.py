from typing import Union

from ....log_pintaformas import log
from ....dependencias import nombres_pygame
from ..evento import Evento, ACTIVAR
from ..tipos import GestorDeEventosPFGeneral
from .teclado import GestorEventosTecladoFlecha


class GestorDeEventosFlecha(GestorDeEventosPFGeneral):
    clase_gestor_teclado = GestorEventosTecladoFlecha

    def evaluar_movimiento_raton(self, evento: Evento) -> None:
        pass

    def evaluar_otros_eventos(self, evento: Evento, tipo_evento: Union[str, int]) -> None:

        if evento == ACTIVAR:
            log.anotar('ACTIVAR recibido en GestorDeEventosFlecha')

        elif tipo_evento == nombres_pygame.MOUSEBUTTONDOWN:
            log.anotar(f'Herramienta seleccion: click en {evento.posicion}')
            posicion_en_documento = self.realizador.vista.visualizacion.aplicar_zoom(evento.posicion, inverso=True)
            log.anotar(f'posicion en documento {posicion_en_documento}')
            self.realizador.seleccionar_por_posicion(evento.posicion)
        else:
            pass
