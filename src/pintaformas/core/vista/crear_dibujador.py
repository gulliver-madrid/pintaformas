from ..general.control_capas import ControlDeCapas
from .areas.area_dibujo import AreaDibujo
from .dibujador import DibujadorAreaDibujo
from .visualizacion import Visualizacion


def crear_dibujador_area_dibujo(
        area_dibujo: AreaDibujo,
        visualizacion: Visualizacion,
        control_capas: ControlDeCapas
        ) -> DibujadorAreaDibujo:

    dibujador = DibujadorAreaDibujo(
        area_dibujo.dimensiones,
        visualizacion,
        area_dibujo.capas.capa_dibujo,
        area_dibujo.capas.capa_cursor,
        area_dibujo.capas.capa_seleccion,
        control_capas
    )
    return dibujador
