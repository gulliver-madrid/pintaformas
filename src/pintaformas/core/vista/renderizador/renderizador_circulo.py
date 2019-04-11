from ....core.vista.surfaces import GenericSurface
from ... import cfg
from ...elementos.formas import Circulo
from ...elementos.seleccion import Seleccion
from ...tipos import (Color, Dimensiones, PosicionEnPantalla, Tuple2Int,
                      convertir_a_tupla_dos_int)
from ..capas.capa import CapaIndividual
from .renderizador_base import RenderizadorBase

DIMS = X, Y = 0, 1

ANCHO_CIRCUNFERENCIA = 2  # era 5, se refiere al ancho que tiene la linea de seleccion del circulo en pantalla
ANCHO_SELECCION = 3


class RenderizadorCirculo(RenderizadorBase):
    __slots__ = ()

    def actualizar_surface_seleccion_circulo(self, capa: CapaIndividual) -> None:
        if not capa.surface:
            capa.surface = self._operador_grafico.crear_surface(self._area_dibujo.rect.size)
        capa.posicion_capa = PosicionEnPantalla((0, 0))
        capa.reestablecer_fondo()
        seleccion = self._diccionario_objetos.get_item(capa.codigo)
        assert isinstance(seleccion, Seleccion)
        circulo = seleccion.objeto_seleccionado
        assert isinstance(circulo, Circulo)
        self.mostrar_circulo_seleccionado(capa, circulo)


    def mostrar_circulo_seleccionado(self, capa: CapaIndividual, circulo: Circulo) -> None:
        '''
        Hay que tener en cuenta que el ancho se calcula desde el borde hacia dentro.
        '''
        assert capa.surface
        posicion = self._visualizacion.pasar_a_pantalla(circulo.posicion)  # posicion_pantalla
        radio = self._visualizacion.aplicar_zoom(circulo.radio)  # radio_en_pantalla
        ancho = ANCHO_CIRCUNFERENCIA  # ancho_en_pantalla
        if radio < ancho:
            radio = ancho
        self._mostrar_circulo_seleccionado_en_pantalla(
            capa.surface,
            circulo.color,
            posicion,
            radio,
            ancho
        )


    def _mostrar_circulo_seleccionado_en_pantalla(self,
            surface: GenericSurface,
            color: Color,
            posicion: PosicionEnPantalla,
            radio: int,
            ancho: int) -> None:
        '''
        Todos los valores son en pantalla
        color es el color del circulo
        color_seleccion es un color predeterminado para la seleccion
        '''
        color_seleccion = Color(cfg.COLOR_SELECCION)
        self._operador_grafico.dibujar_circulo(surface, color_seleccion, posicion, radio + ANCHO_SELECCION, ANCHO_SELECCION)
        self._operador_grafico.dibujar_circulo(surface, color, posicion, radio, ancho)


    def actualizar_surface_circulo(self, capa: CapaIndividual) -> None:
        circulo = self._diccionario_objetos.get_item(capa.codigo)
        assert isinstance(circulo, Circulo)
        posicion = self._visualizacion.pasar_a_pantalla(circulo.posicion)  # posicion_pantalla
        radio = self._visualizacion.aplicar_zoom(circulo.radio)  # radio_en_pantalla

        if self._hay_que_redefinir_surface(posicion, radio, capa):
            capa.surface = self._redefinir_surface(radio)
        assert capa.surface
        capa.reestablecer_fondo()
        capa.posicion_capa = posicion.restar_entero(radio)
        posicion_interna = (radio, radio)
        self._operador_grafico.dibujar_circulo(capa.surface, circulo.color, posicion_interna, radio)

    def _redefinir_surface(self, radio: int) -> GenericSurface:
        tamano_area_dibujo = self._area_dibujo.rect.size
        dimensiones_capa_circulo = Dimensiones(
            min(radio * 2, tamano_area_dibujo[dim]) for dim in DIMS
        )
        return self._operador_grafico.crear_surface(dimensiones_capa_circulo)


    def _hay_que_redefinir_surface(self, posicion: PosicionEnPantalla, radio: int, capa: CapaIndividual) -> bool:
        '''Si no tiene surface o si el circulo se sale de la capa
        (Aunque quizas esto podria suceder por estar fuera del area de dibujo)
        '''
        bottom_right = convertir_a_tupla_dos_int(posicion.sumar_entero(radio))
        if not capa.surface:
            return True
        return esta_fuera(bottom_right, capa.surface)


def esta_fuera(punto: Tuple2Int, surface: GenericSurface) -> bool:
    rect = surface.get_rect()
    return not rect.collidepoint(punto)
