from typing import Union
from ....dependencias import nombres_pygame
from ...tipos import PosicionEnPantalla
from .teclado import GestorEventosTecladoRecta
from ..tipos import GestorDeEventosPFGeneral

# TYPE_CHECKING
from ..evento import Evento

X, Y = 0, 1


class GestorDeEventosRecta(GestorDeEventosPFGeneral):
    clase_gestor_teclado = GestorEventosTecladoRecta

    def evaluar_movimiento_raton(self, evento: Evento) -> None:
        if self.realizador.lapiz.trazo_iniciado:
            self.realizador.lapiz.mantener_trazo_recto(evento.posicion)


    def evaluar_otros_eventos(self, evento: Evento, tipo_evento: Union[str, int]) -> None:
        if tipo_evento == 'DESACTIVAR':
            self.realizador.abandonar_recta()
        elif tipo_evento == nombres_pygame.MOUSEBUTTONDOWN:
            if self.realizador.lapiz.trazo_iniciado:
                self.establecer_punto_intermedio(evento.posicion)
            else:
                separacion_vertical = self.realizador.vista.separacion_vertical
                if evento.posicion[Y] < separacion_vertical:
                    self.realizador.lapiz.iniciar_trazo(evento.posicion)


    def establecer_punto_intermedio(self, posicion: PosicionEnPantalla) -> None:
        self.realizador.finalizar_segmento_recta(posicion)
        self.realizador.lapiz.iniciar_trazo(posicion)
