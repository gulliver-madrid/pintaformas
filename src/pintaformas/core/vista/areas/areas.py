from typing import Sequence

from .area import AreaAutoactualizable
from .area_dibujo import AreaDibujo
from .area_informativa import AreaInformativa
from .area_herramientas import AreaHerramientas
from .area_muestras_colores import AreaMuestrasColores
from .area_color_seleccionado import AreaColorSeleccionado


class Areas:
    def __init__(self,
            dibujo: AreaDibujo,
            herramientas: AreaHerramientas,
            informativa: AreaInformativa,
            muestras_colores: AreaMuestrasColores,
            color_seleccionado: AreaColorSeleccionado):
        self.dibujo = dibujo
        self.herramientas = herramientas
        self.informativa = informativa
        self.muestras_colores = muestras_colores
        self.color_seleccionado = color_seleccionado

    @property
    def autoactualizables(self) -> Sequence[AreaAutoactualizable]:
        return [self.herramientas, self.informativa, self.muestras_colores, self.color_seleccionado]
