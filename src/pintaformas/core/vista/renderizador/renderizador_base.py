from typing import Final
from ...general.control_capas import MappingToObjetosParaRenderizador
from ..areas.area_dibujo import AreaDibujo
from ..componentes_renderizador import ComponentesRenderizador
from ..operador_grafico import OperadorGrafico
from ..operador_grafico_sistema import OperadorGraficoSistema
from ..visualizacion import Visualizacion


class RenderizadorBase:
    __slots__ = ('_area_dibujo', '_visualizacion', '_operador_grafico', '_operador_grafico_sistema', '_diccionario_objetos',)
    _area_dibujo: AreaDibujo
    _visualizacion: Final[Visualizacion]
    _operador_grafico: Final[OperadorGrafico]
    _operador_grafico_sistema: Final[OperadorGraficoSistema]
    _diccionario_objetos: MappingToObjetosParaRenderizador

    def __init__(self, componentes: ComponentesRenderizador) -> None:
        self._area_dibujo = componentes.area_dibujo
        self._visualizacion = componentes.visualizacion
        self._operador_grafico = componentes.operador_grafico
        self._operador_grafico_sistema = componentes.operador_grafico_sistema
        self._diccionario_objetos = componentes.diccionario_objetos
