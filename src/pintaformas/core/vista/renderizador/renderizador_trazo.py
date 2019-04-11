from ...elementos.formas import Linea
from ...tipos import Color, Dimensiones
from ..capas.capa import CapaIndividual
from ..componentes_renderizador import ComponentesRenderizador
from .renderizador_base import RenderizadorBase
from .reposicionador import Reposicionador

MOSTRAR_FONDO_CAPA_PARA_DEBUG = 0


class RenderizadorTrazo(RenderizadorBase):
    __slots__ = ('reposicionador')
    reposicionador: Reposicionador

    def __init__(self, componentes_renderizador: ComponentesRenderizador):
        super().__init__(componentes_renderizador)
        self.reposicionador = Reposicionador()

    def actualizar_surface_trazo(self, capa: CapaIndividual) -> None:
        linea = self._diccionario_objetos.get_item(capa.codigo)

        assert isinstance(linea, Linea)
        origen = self._visualizacion.pasar_a_pantalla(linea.origen)
        destino = self._visualizacion.pasar_a_pantalla(linea.destino)
        grosor = self._visualizacion.aplicar_zoom(linea.grosor)
        dim_maximas = Dimensiones(self._area_dibujo.rect.size)
        capa.posicion_capa, dimensiones_capa, origen_interno, destino_interno = self.reposicionador.hallar_posicion_y_dimensiones_capa(origen, destino, grosor, dim_maximas)
        capa.surface = self._operador_grafico.crear_surface(dimensiones_capa)
        assert capa.surface
        capa.reestablecer_fondo()
        if MOSTRAR_FONDO_CAPA_PARA_DEBUG:
            capa.surface.fill(Color((255, 255, 0)))  # debug
        self._operador_grafico.dibujar_linea(
            capa.surface,
            linea.color,
            origen_interno,
            destino_interno,
            grosor
        )
