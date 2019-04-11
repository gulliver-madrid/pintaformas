from typing import Union
from ....dependencias import nombres_pygame, PygameRect
from ...tipos import PosicionEnPantalla
from ..excepciones_eventos import EventoUsado
from .teclado import GestorEventosTecladoUniversal
from ..tipos import GestorDeEventosPFGeneral

# TYPE_CHECKING
from ..evento import Evento

X, Y = 0, 1


class GestorDeEventosUniversal(GestorDeEventosPFGeneral):
    clase_gestor_teclado = GestorEventosTecladoUniversal

    def evaluar_movimiento_raton(self, evento: Evento) -> None:
        self.realizador.mover_cursor(evento.posicion)

    def evaluar_otros_eventos(self, evento: Evento, tipo_evento: Union[str, int]) -> None:
        # print(f"Evaluando evento {tipo_evento}")
        if tipo_evento == nombres_pygame.MOUSEBUTTONDOWN:
            self._modos.establecer('boton_pulsado', True)
            self._evaluar_seleccion_de_color(evento.posicion)
            self._evaluar_seleccion_de_herramienta(evento.posicion)

            for i, rect in enumerate(self.realizador.vista.areas.herramientas.rects_herramientas):
                if rect.collidepoint(*evento.posicion):
                    if i != self.realizador.vista.areas.herramientas.herramienta_seleccionada:
                        self.realizador.seleccionar_herramienta(i)
                        raise EventoUsado()

        elif tipo_evento == nombres_pygame.VIDEORESIZE:
            # Este evento se genera despues de un redimensionamiento de la ventana por el usuario
            assert isinstance(evento.size, tuple)
            ancho, alto = evento.size
            assert isinstance(ancho, int)
            assert isinstance(alto, int)
            self.realizador.redimensionar_contenido_ventana()

        elif tipo_evento == nombres_pygame.MOUSEBUTTONUP:
            self._modos.establecer('boton_pulsado', False)

        elif tipo_evento == nombres_pygame.ACTIVEEVENT:
            if not hasattr(evento, 'gain'):
                return
            if evento.gain == 0:
                self.realizador.set_visibilidad_general_cursor(False)
            elif evento.gain == 1:
                self.realizador.set_visibilidad_general_cursor(True)

        elif tipo_evento == nombres_pygame.QUIT:
            self.realizador.salir()


    def _evaluar_seleccion_de_color(self, posicion_clicada: PosicionEnPantalla) -> None:
        color_actual = self.realizador.vista.areas.color_seleccionado.color_seleccionado

        muestras_colores = self.realizador.vista.areas.muestras_colores
        assert muestras_colores.rects_colores
        rect: PygameRect
        for indice, rect in enumerate(muestras_colores.rects_colores):
            if rect.collidepoint(posicion_clicada):
                color_clicado = muestras_colores.colores_muestras[indice]
                if color_clicado != color_actual:
                    self.realizador.seleccionar_color(color_clicado)
                raise EventoUsado()

    def _evaluar_seleccion_de_herramienta(self, posicion_clicada: PosicionEnPantalla) -> None:
        for i, rect in enumerate(self.realizador.vista.areas.herramientas.rects_herramientas):
            if rect.collidepoint(posicion_clicada):
                if i != self.realizador.vista.areas.herramientas.herramienta_seleccionada:
                    self.realizador.seleccionar_herramienta(i)
                    raise EventoUsado()
