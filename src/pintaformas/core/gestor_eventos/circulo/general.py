from typing import Union

from ....dependencias import nombres_pygame
from ...elementos.forma import Forma
from ..evento import Evento
from ..tipos import GestorDeEventosPFGeneral
from .teclado import GestorEventosTecladoSeleccionCirculo


class GestorDeEventosSeleccionCirculo(GestorDeEventosPFGeneral):
    clase_gestor_teclado = GestorEventosTecladoSeleccionCirculo

    def evaluar_movimiento_raton(self, evento: Evento) -> None:
        if self._modos.obtener_valor('boton_pulsado'):
            if self.realizador.gestor_seleccion.seleccion.objeto_seleccionado:
                self.realizador.gestor_seleccion_circulo.modifica_circulo_recien_creado(evento.posicion)
        self.realizador.mover_cursor(evento.posicion)


    def evaluar_otros_eventos(self, evento: Evento, tipo_evento: Union[str, int]) -> None:
        if tipo_evento == 'ACTIVAR':
            pass
        elif tipo_evento == nombres_pygame.MOUSEBUTTONDOWN:
            # TODO:  ¿No deberiamos circunscribirnos al area de dibujo?
            self.realizador.gestor_seleccion_circulo.crea_circulo(evento.posicion)
        elif tipo_evento == nombres_pygame.MOUSEBUTTONUP and self.realizador.gestor_seleccion.seleccion.objeto_seleccionado:
            objeto_seleccionado = self.realizador.gestor_seleccion.seleccion.objeto_seleccionado
            assert isinstance(objeto_seleccionado, Forma)
            if objeto_seleccionado.tipo == 'circulo':
                self.realizador.estampar_circulo()



    def __sin_acceso(self, evento: Evento) -> None:
        # No hay acceso a esta funcion
        self.realizador.gestor_seleccion_circulo.mover_circulo(evento.posicion)
