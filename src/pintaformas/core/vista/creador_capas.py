from typing import Sequence

from ...log_pintaformas import log
from ..tipos import Tuple3Int, CodigoObjetoEspecial
from ..elementos.objeto_modelo import ObjetosModelo
from ..elementos import Lienzo
from ..general.control_capas import ControlDeCapas, ControlObjetosVista
from .areas.area_dibujo import AreaDibujo
from .areas.area_informativa import AreaInformativa
from .areas.area_herramientas import AreaHerramientas, CargadorDeImagenes, CreadorImagenDesdeCaracter
from .areas.adaptadores import CreadorPanelHerramientasPintaFormas, CreadorMuestrasPintaFormas
from .areas.area_muestras_colores import AreaMuestrasColores
from .areas.area_color_seleccionado import AreaColorSeleccionado
from .areas.areas import Areas
from .areas.area import Area
from .capas import CapaContenedora, CapaIndividual
from .capas.capas_area_dibujo import CapasAreaDibujo
from .creador_rects_areas import CreadorRectsAreas
from .visualizacion import Visualizacion
from .surfaces import GenericSurfaceFactory


class CreadorDeCapas:
    control_objetos_vista: ControlObjetosVista
    surface_factory: GenericSurfaceFactory

    def __init__(self,
     surface_factory: GenericSurfaceFactory,
            creador_rects_areas: CreadorRectsAreas,
            visualizacion: Visualizacion,
            colores_muestras: Sequence[Tuple3Int],
            objetos_modelo: ObjetosModelo,
            control_capas: ControlDeCapas):
        self.surface_factory = surface_factory
        self.visualizacion = visualizacion
        self.creador_rects_areas = creador_rects_areas
        self.colores_muestras = colores_muestras
        self.objetos_modelo = objetos_modelo
        self.control_capas = control_capas
        self.control_cambios = control_capas.control_cambios
        self.control_objetos_vista = control_capas.control_objetos_vista


    def crear_areas_principales(self) -> tuple[Areas, dict[str, Area]]:
        area_dibujo = self._crear_area_dibujo()
        area_informativa = AreaInformativa()
        creador_panel_herramientas=CreadorPanelHerramientasPintaFormas(self.surface_factory)
        cargador_imagenes= CargadorDeImagenes(self.surface_factory)
        creador_imagenes_desde_caracter=CreadorImagenDesdeCaracter(self.surface_factory)
        area_herramientas = AreaHerramientas(creador_panel_herramientas,cargador_imagenes,creador_imagenes_desde_caracter)
        creador_muestras = CreadorMuestrasPintaFormas(self.surface_factory)
        area_color_seleccionado = AreaColorSeleccionado(creador_muestras)
        area_muestras_colores = AreaMuestrasColores(creador_muestras, self.colores_muestras)
        areas = Areas(
            dibujo=area_dibujo,
            informativa=area_informativa,
            herramientas=area_herramientas,
            color_seleccionado=area_color_seleccionado,
            muestras_colores=area_muestras_colores,
        )
        dicc_areas: dict[str, Area] = dict(
            dibujo=area_dibujo,
            informativa=area_informativa,
            herramientas=area_herramientas,
            color_seleccionado=area_color_seleccionado,
            muestras_colores=area_muestras_colores,
        )
        for area in dicc_areas.values():
            self.control_cambios.registrar(area.codigo)
            self.control_objetos_vista.anadir_capa(area)

        self.creador_rects_areas.anadir_rects(dicc_areas)
        log.anotar('Se crearon las areas principales')
        return areas, dicc_areas


    def _crear_area_dibujo(self) -> AreaDibujo:
        lienzo = Lienzo()
        seleccion = self.objetos_modelo['seleccion']
        cursor = self.objetos_modelo['cursor']

        capas_area_dibujo = CapasAreaDibujo(
            capa_lienzo=CapaIndividual(CodigoObjetoEspecial.lienzo),
            capa_dibujo=CapaContenedora(CodigoObjetoEspecial.dibujo),
            capa_seleccion=CapaIndividual(CodigoObjetoEspecial.seleccion),
            capa_cursor=CapaIndividual(CodigoObjetoEspecial.cursor)
        )

        self.control_objetos_vista.anadir_objeto_vectorial(lienzo)
        self.control_objetos_vista.anadir_objeto_vectorial(seleccion)
        self.control_objetos_vista.anadir_objeto_vectorial(cursor)
        for capa in capas_area_dibujo.todas:
            self.control_cambios.registrar(capa.codigo)
            self.control_objetos_vista.anadir_capa(capa)

        return AreaDibujo(capas_area_dibujo, self.control_cambios)
