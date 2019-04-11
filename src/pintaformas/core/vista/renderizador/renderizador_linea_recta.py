from ....core.vista.surfaces import GenericSurface
from ... import cfg
from ...elementos.formas import Linea
from ...elementos.seleccion import Seleccion
from ...tipos import Color
from ..capas.capa import CapaIndividual
from ..componentes_renderizador import ComponentesRenderizador
from .renderizador_base import RenderizadorBase
from .reposicionador import Reposicionador

ANCHO_SELECCION = 3  # era 5, se refiere al ancho que tiene la linea de seleccion del circulo en pantalla
DIMS = X, Y = 0, 1


class RenderizadorLineaRecta(RenderizadorBase):
    __slots__ = ('color_seleccion', 'reposicionador')
    color_seleccion: Color
    reposicionador: Reposicionador

    def __init__(self, componentes_renderizador: ComponentesRenderizador):
        super().__init__(componentes_renderizador)
        self.color_seleccion = Color(cfg.COLOR_SELECCION)
        self.reposicionador = Reposicionador()


    def actualizar_surface_seleccion_linea_recta(self, capa: CapaIndividual) -> None:
        seleccion = self._diccionario_objetos.get_item(capa.codigo)
        assert isinstance(seleccion, Seleccion)
        linea = seleccion.objeto_seleccionado
        assert isinstance(linea, Linea)
        if not capa.surface:
            capa.surface = self._operador_grafico.crear_surface(self._area_dibujo.rect.size)
        assert capa.surface
        capa.reestablecer_fondo()
        self._mostrar_linea_seleccionada(capa.surface, linea)


    def _mostrar_linea_seleccionada(self, surface: GenericSurface, linea: Linea) -> None:
        '''
        Hay que tener en cuenta que el ancho se calcula desde el borde hacia dentro.
        '''

        origen_en_pantalla = self._visualizacion.pasar_a_pantalla(linea.origen)
        grosor_en_pantalla = self._visualizacion.aplicar_zoom(linea.grosor)
        destino_en_pantalla = self._visualizacion.pasar_a_pantalla(linea.destino)

        self._operador_grafico.dibujar_linea(
            surface,
            self.color_seleccion,
            origen_en_pantalla.restar_entero(ANCHO_SELECCION),
            destino_en_pantalla.sumar_entero(ANCHO_SELECCION),
            grosor_en_pantalla + ANCHO_SELECCION * 2
        )
        self._operador_grafico.dibujar_linea(
            surface,
            linea.color,
            origen_en_pantalla,
            destino_en_pantalla,
            grosor_en_pantalla
        )
