from typing import Final, Iterable, Sequence, Union

from ...elementos.cursor import Cursor, TipoCursor
from ...elementos.forma import Forma
from ...elementos.lienzo import Lienzo
from ...elementos.seleccion import Seleccion
from ...tipos import (CodigoElementoVista, CodigoObjetoEspecial,
                      convertir_a_tupla_dos_int)
from ..areas.area_dibujo import AreaDibujo
from ..capas import Capa, CapaContenedora, CapaIndividual
from ..componentes_renderizador import ComponentesRenderizador
from ..objeto_capas_internas import ObjetoConCapasInternas
from ..operador_grafico import SurfaceConPosicion
from .renderizador_base import RenderizadorBase
from .renderizador_circulo import RenderizadorCirculo
from .renderizador_linea_recta import RenderizadorLineaRecta
from .renderizador_trazo import RenderizadorTrazo

CAPAS_QUE_DEPENDEN_DEL_ZOOM = ('dibujo', 'seleccion')  # TODO: usarlo o borrarlo


class Renderizador(RenderizadorBase):
    __slots__ = ('renderizador_trazo', 'renderizador_circulo', 'renderizador_seleccion_linea_recta')
    renderizador_trazo: Final[RenderizadorTrazo]
    renderizador_circulo: Final[RenderizadorCirculo]
    renderizador_seleccion_linea_recta: Final[RenderizadorLineaRecta]

    def __init__(self, componentes_renderizador: ComponentesRenderizador):
        super().__init__(componentes_renderizador)
        self.renderizador_trazo = RenderizadorTrazo(componentes_renderizador)
        self.renderizador_circulo = RenderizadorCirculo(componentes_renderizador)
        self.renderizador_seleccion_linea_recta = RenderizadorLineaRecta(componentes_renderizador)


    def renderizar_simple(self, capa: Union[Capa, ObjetoConCapasInternas]) -> None:
        '''
        Renderiza una capa. Si es contenedora, consolida sus capas hijas.
        '''

        if hasattr(capa, 'capas_internas'):
            assert isinstance(capa, (CapaContenedora, AreaDibujo))
            self._renderizar_capa_contenedora(capa)
        else:
            assert isinstance(capa, CapaIndividual)
            self._actualizar_surface_capa(capa)


    def _renderizar_capa_contenedora(self, capa: ObjetoConCapasInternas) -> None:
        if not capa.surface:
            if isinstance(capa, AreaDibujo):
                capa.surface = self._operador_grafico_sistema.obtener_subsurface_ventana(capa.rect)
            else:
                capa.surface = self._operador_grafico.crear_surface(capa.dimensiones)

        capa.reestablecer_fondo()

        surfaces_con_posiciones = obtener_surfaces_con_posiciones(capa.capas_internas)
        self._operador_grafico.pegar_capas(capa, surfaces_con_posiciones)


    def _actualizar_surface_capa(self, capa: CapaIndividual) -> None:
        """Actualiza el surface de una capa individual, que puede corresponder con el lienzo, la seleccion, el cursor o una forma."""
        tipo_capa = capa.tipo_de_capa
        assert tipo_capa == 'individual'
        assert isinstance(capa, CapaIndividual)
        codigo = capa.codigo
        if codigo == CodigoObjetoEspecial.lienzo:
            self._actualizar_surface_lienzo(capa)
        elif codigo == CodigoObjetoEspecial.seleccion:
            self._renderizar_seleccion(capa)
        elif codigo == CodigoObjetoEspecial.cursor:
            self._renderizar_cursor(capa)
        else:
            self._renderizar_forma(capa, codigo)

    def _renderizar_forma(self, capa: CapaIndividual, codigo: CodigoElementoVista) -> None:
        forma = self._diccionario_objetos.get_item(codigo)
        assert isinstance(forma, Forma), forma
        tipo_de_forma = forma.tipo
        if tipo_de_forma in ('trazo', 'linea'):  # creo que es lo mismo
            self.renderizador_trazo.actualizar_surface_trazo(capa)
        elif tipo_de_forma == 'circulo':
            self.renderizador_circulo.actualizar_surface_circulo(capa)
        else:
            raise NotImplementedError(f'{tipo_de_forma}')

    def _renderizar_seleccion(self, capa: CapaIndividual) -> None:
        seleccion = self._diccionario_objetos.get_item(capa.codigo)
        assert isinstance(seleccion, Seleccion)
        if seleccion.objeto_seleccionado == None:
            capa.surface = None
        else:
            forma = seleccion.objeto_seleccionado
            assert isinstance(forma, Forma)
            tipo_de_forma = forma.tipo
            if tipo_de_forma == 'circulo':
                self.renderizador_circulo.actualizar_surface_seleccion_circulo(capa)
            elif tipo_de_forma == 'linea':
                self.renderizador_seleccion_linea_recta.actualizar_surface_seleccion_linea_recta(capa)
            else:
                raise RuntimeError(f'Tipo de forma no aceptada: {tipo_de_forma}')


    def _actualizar_surface_lienzo(self, capa: CapaIndividual) -> None:
        if not capa.surface:
            capa.surface = self._operador_grafico.crear_surface(self._area_dibujo.dimensiones)
        assert capa.surface
        capa.reestablecer_fondo()
        lienzo = self._diccionario_objetos.get_item(capa.codigo)
        assert isinstance(lienzo, Lienzo), f'{lienzo}, {self._diccionario_objetos}'
        top_left = self._visualizacion.pasar_a_pantalla(lienzo.posicion)
        dimensiones_en_pantalla = self._visualizacion.aplicar_zoom(
            convertir_a_tupla_dos_int(lienzo.dimensiones_lienzo)
        )
        rect_lienzo = convertir_a_tupla_dos_int(top_left) + dimensiones_en_pantalla
        self._operador_grafico.dibujar_rectangulo(capa.surface, lienzo.color, rect_lienzo)


    def _renderizar_cursor(self, capa: CapaIndividual) -> None:
        cursor = self._diccionario_objetos.get_item(capa.codigo)
        assert isinstance(cursor, Cursor)
        mostrar_cursor_so = cursor.visibilidad_cursor_so
        self._operador_grafico_sistema.mostrar_cursor_sistema_operativo(mostrar_cursor_so)
        if cursor.visibilidad_cursor_manual == False:
            capa.surface = None
            return

        assert cursor.visibilidad_cursor_manual == True
        if cursor.tipo_cursor == TipoCursor.flecha:
            capa.surface = None
            self._operador_grafico_sistema.mostrar_cursor_sistema_operativo(True)
            return

        assert cursor.tipo_cursor == TipoCursor.pintura
        if not capa.surface:
            capa.surface = self._operador_grafico.crear_surface((cursor.radio * 2, cursor.radio * 2))
        capa.reestablecer_fondo()
        capa.posicion_capa = cursor.posicion.restar_entero(cursor.radio)
        self._operador_grafico.dibujar_circulo(
            capa.surface, cursor.color, (cursor.radio, cursor.radio), cursor.radio
        )


def get_surface_con_posicion(capa: Capa) -> SurfaceConPosicion:
    assert capa.surface
    assert capa.posicion_capa
    return (capa.surface, capa.posicion_capa)


def obtener_surfaces_con_posiciones(capas: Sequence[Capa]) -> Iterable[SurfaceConPosicion]:
    return (get_surface_con_posicion(capa) for capa in capas if capa.surface)
