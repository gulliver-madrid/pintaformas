from typing import Union
from ....dependencias import nombres_pygame
from ..evento import Evento
from ..tipos import GestorDeEventosPFGeneral
from .teclado import GestorEventosTecladoNormal


DIMS = X, Y = 0, 1

class GestorDeEventosNormal(GestorDeEventosPFGeneral):
    clase_gestor_teclado = GestorEventosTecladoNormal

    def evaluar_movimiento_raton(self, evento: Evento) -> None:

        if self._modos.obtener_valor('boton_pulsado'):
            self.realizador.set_ocultamiento_cursor_mientras_se_dibuja(True)
            origen = evento.posicion.restar(evento.desplazamiento)
            self.realizador.lapiz.realizar_trazo(origen, evento.posicion)



    def evaluar_otros_eventos(self, evento: Evento, tipo_evento: Union[str, int]) -> None:

        if tipo_evento == nombres_pygame.MOUSEBUTTONUP:
            self.realizador.set_ocultamiento_cursor_mientras_se_dibuja(False)
