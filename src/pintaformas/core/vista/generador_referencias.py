from dataclasses import dataclass

from ...core.vista.surfaces import GenericSurface
from ..tipos import Dimensiones
from .operador_grafico_sistema import OperadorGraficoSistema


@dataclass
class ReferenciasClave:
    ancho_ventana: int
    alto_ventana: int
    separacion_vertical: int

    def get_values(self) -> tuple[int, int, int]:
        return self.ancho_ventana, self.alto_ventana, self .separacion_vertical


class GeneradorReferenciasClaveVista:
    def __init__(self, operador_grafico_sistema: OperadorGraficoSistema):
        self._operador_grafico_sistema = operador_grafico_sistema

    def obtener_referencias_clave(self, *, porcentaje_separacion_vertical: float) -> ReferenciasClave:
        ventana = self._operador_grafico_sistema.obtener_surface_principal()
        ancho_ventana, alto_ventana = self.obtener_dimensiones_ventana(ventana)
        separacion_vertical = self.obtener_separacion_vertical(alto_ventana, porcentaje_separacion_vertical)
        referencias_clave = ReferenciasClave(
            ancho_ventana=ancho_ventana,
            alto_ventana=alto_ventana,
            separacion_vertical=separacion_vertical,
        )
        return referencias_clave

    @staticmethod
    def obtener_dimensiones_ventana(ventana: GenericSurface) -> Dimensiones:
        return Dimensiones(ventana.get_size())

    @staticmethod
    def obtener_separacion_vertical(alto_ventana: int, porcentaje_separacion: float) -> int:
        return round(porcentaje_separacion * alto_ventana)
