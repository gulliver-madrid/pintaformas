from ..colores import COLORES_MUESTRAS
from .creador_capas import CreadorDeCapas
from .creador_rects_areas import CreadorRectsAreas
from .generador_referencias import GeneradorReferenciasClaveVista
from .surfaces import GenericSurfaceFactory
from .vista import Vista
from .visualizacion import Visualizacion

# TYPE_CHECKING
from .operador_grafico import OperadorGrafico
from .operador_grafico_sistema import OperadorGraficoSistema
from ..elementos.objeto_modelo import ObjetosModelo
from ..general.control_capas import ControlDeCapas

def crear_vista(
        surface_factory: GenericSurfaceFactory,
        objetos_modelo: ObjetosModelo,
        control_capas: ControlDeCapas
        ) -> Vista:
    operador_grafico = OperadorGrafico(surface_factory)
    visualizacion = Visualizacion()
    operador_grafico_sistema = OperadorGraficoSistema(surface_factory)
    generador_refs_clave = GeneradorReferenciasClaveVista(operador_grafico_sistema)
    creador_rects_areas = CreadorRectsAreas(generador_refs_clave, control_capas)

    creador_capas = CreadorDeCapas(surface_factory, creador_rects_areas, visualizacion, COLORES_MUESTRAS, objetos_modelo, control_capas)

    return Vista(operador_grafico, operador_grafico_sistema, visualizacion, creador_capas, control_capas)
