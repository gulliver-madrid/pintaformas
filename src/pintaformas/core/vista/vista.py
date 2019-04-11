from typing import Optional, Sequence

from ...dependencias import PygameRect
from ...log_pintaformas import cat, log
from ..general.control_cambios import ControlDeCambios
from ..general.control_capas import (ControlDeCapas, MappingToObjetosParaRenderizador)
from ..tipos import PosicionEnPantalla
from .areas.area import Area
from .areas.areas import Areas
from .componentes_renderizador import ComponentesRenderizador
from .creador_capas import CreadorDeCapas
from .crear_dibujador import crear_dibujador_area_dibujo
from .dibujador import DibujadorAreaDibujo
from .operador_grafico import OperadorGrafico
from .operador_grafico_sistema import OperadorGraficoSistema
from .renderizador import Renderizador
from .visualizacion import Visualizacion
from .renderizador_general import RenderizadorGeneral

ACTUALIZAR_TROZO_PEQUENO = False  # mut: skip line
RECT_PEQUENO = PygameRect(0, 0, 100, 100)  # mut: skip line

DiccAreas = dict[str, Area]
_Delayed_Areas = Optional[Areas]
_Delayed_DiccAreas = Optional[DiccAreas]


class Vista:
    __slots__ = ('operador_grafico', 'operador_grafico_sistema', 'visualizacion', 'creador_capas', 'control_capas', 'control_cambios', 'diccionario_objetos', '_dicc_areas', '_areas', 'dibujador', '_renderizador_general')
    operador_grafico: OperadorGrafico
    operador_grafico_sistema: OperadorGraficoSistema
    visualizacion: Visualizacion
    creador_capas: CreadorDeCapas
    control_capas: ControlDeCapas
    control_cambios: ControlDeCambios
    diccionario_objetos: MappingToObjetosParaRenderizador
    _renderizador_general: RenderizadorGeneral
    dibujador: DibujadorAreaDibujo
    _areas: _Delayed_Areas
    _dicc_areas: _Delayed_DiccAreas

    def __init__(self,
            operador_grafico: OperadorGrafico,
            operador_grafico_sistema: OperadorGraficoSistema,
            visualizacion: Visualizacion,
            creador_capas: CreadorDeCapas,
            control_capas: ControlDeCapas):
        self.operador_grafico = operador_grafico
        self.operador_grafico_sistema = operador_grafico_sistema
        self.visualizacion = visualizacion
        self.creador_capas = creador_capas
        self.control_capas = control_capas
        self.control_cambios = control_capas.control_cambios
        self.diccionario_objetos = control_capas.control_objetos_vista.get_diccionario_objetos_para_renderizador()
        self._areas = None
        self._dicc_areas = None

    @property
    def areas(self) -> Areas:
        assert (areas := self._areas)
        return areas

    @property
    def dicc_areas(self) -> DiccAreas:
        assert (dicc_areas := self._dicc_areas)
        return dicc_areas

    @property
    def separacion_vertical(self) -> int:
        return self.creador_capas.creador_rects_areas.referencias_clave.separacion_vertical

    def crear_areas_principales(self) -> None:
        self._areas, self._dicc_areas = self.creador_capas.crear_areas_principales()

    def iniciar_renderizador(self) -> None:
        self.dibujador = crear_dibujador_area_dibujo(self.areas.dibujo, self.visualizacion, self.control_capas)
        componentes_renderizador = ComponentesRenderizador(
            self.diccionario_objetos, self.operador_grafico, self.operador_grafico_sistema, self.areas.dibujo, self.visualizacion
        )
        renderizador = Renderizador(componentes_renderizador)
        self._renderizador_general = RenderizadorGeneral(
            self.operador_grafico, self.operador_grafico_sistema, renderizador, self.areas, self.control_capas
        )
        self.visualizacion.establecer_centro_base(PosicionEnPantalla(self.areas.dibujo.rect.center))

    def actualizar_cambios(self) -> None:
        if self.control_cambios.hay_cambios_pendientes():
            log.anotar('\nActualizando surfaces', cat.vista)
            self._renderizador_general.renderizar()
            args: Sequence[PygameRect]
            if ACTUALIZAR_TROZO_PEQUENO:
                args = [RECT_PEQUENO]
            else:
                args = []
            self.operador_grafico_sistema.actualizar_pantalla(*args)
            log.anotar('Actualizando pantalla\n', cat.vista)

    def poner_titulo(self, titulo: str) -> None:
        self.operador_grafico_sistema.poner_titulo(titulo)
