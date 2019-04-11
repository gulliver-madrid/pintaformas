from typing import Sequence

from ...log_pintaformas import cat, log
from .. import cfg
from ..general.control_capas import ControlDeCapas, ControlObjetosVista
from ..tipos.cev import CodigoStr
from .areas.area import AreaAutoactualizable
from .areas.area_dibujo import AreaDibujo
from .areas.areas import Areas
from .capas import Capa
from .operador_grafico import OperadorGrafico
from .operador_grafico_sistema import OperadorGraficoSistema
from .renderizador import Renderizador
from .revisador_arbol import RevisadorArbol


class RenderizadorGeneral:
    control_objetos_vista: ControlObjetosVista

    def __init__(self,
            operador_grafico: OperadorGrafico,
            operador_grafico_sistema: OperadorGraficoSistema,
            renderizador: Renderizador,
            areas: Areas,
            control_capas: ControlDeCapas):
        self.operador_grafico = operador_grafico
        self.operador_grafico_sistema = operador_grafico_sistema
        self.renderizador = renderizador
        self.areas = areas
        self.control_cambios = control_capas.control_cambios
        self.revisador_arbol = RevisadorArbol(self.control_cambios)
        self.control_objetos_vista = control_capas.control_objetos_vista


    def renderizar(self) -> None:
        '''
        Actualiza los surfaces que lo necesiten segun la informacion de
        control_cambios
        '''
        self._log_contenido_control_cambios()
        codigos_a_renderizar_ordenados = self.revisador_arbol.revisar_arbol(self.areas.dibujo)
        # Estan ordenados porque las capas contenedoras aparecen despues de sus capas hijas
        if cfg.debug_codigos_a_renderizar:
            debug_codigos_a_renderizar(codigos_a_renderizar_ordenados)

        for codigo_str in codigos_a_renderizar_ordenados:
            capa = self.control_objetos_vista.get_capa_by_codigo_str(codigo_str)
            assert isinstance(capa, (Capa, AreaDibujo))
            self.renderizador.renderizar_simple(capa)  # Solo consolida las capas internas de las contenedoras

        for area in self.areas.autoactualizables:
            assert isinstance(area, AreaAutoactualizable)
            if area.codigo in self.control_cambios:
                self._renderizar_area_autoactualizable(area)

        self.control_cambios.vaciar()

    def _renderizar_area_autoactualizable(self, area: AreaAutoactualizable) -> None:
        log.anotar(f'Actualizando {area.codigo}', cat.renderizador)
        if not area.surface:
            subsurface_ventana = self.operador_grafico_sistema.obtener_subsurface_ventana(area.rect)
            area.set_surface(subsurface_ventana)
        area.actualizar_vista()

    def _log_contenido_control_cambios(self) -> None:
        log.anotar(f'Lo que hay en control de cambios: {set(self.control_cambios.debug_modificadas())}', cat.control_cambios)



def debug_codigos_a_renderizar(codigos: Sequence[CodigoStr]) -> None:
    lineas = ["Codigos a renderizar:"]
    for codigo in codigos:
        lineas.append(codigo)
    log.anotar('\n'.join(lineas), cat.renderizador)
