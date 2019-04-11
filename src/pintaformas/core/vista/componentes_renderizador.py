from dataclasses import dataclass

from ..general.control_capas import MappingToObjetosParaRenderizador
from .areas.area_dibujo import AreaDibujo
from .operador_grafico import OperadorGrafico
from .operador_grafico_sistema import OperadorGraficoSistema
from .visualizacion import Visualizacion


@dataclass
class ComponentesRenderizador:
    diccionario_objetos: MappingToObjetosParaRenderizador
    operador_grafico: OperadorGrafico
    operador_grafico_sistema: OperadorGraficoSistema
    area_dibujo: AreaDibujo
    visualizacion: Visualizacion
