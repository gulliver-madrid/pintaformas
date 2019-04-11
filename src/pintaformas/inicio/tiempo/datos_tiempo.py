from typing import Final

from ...core.general.tiempo import convertir_a_milisegundos, Segundos, Milisegundos
from .dato_lag import DatoLag, NumCiclo

NumCicloToDatoLag = dict[NumCiclo, DatoLag]

COEFICIENTE_LIMITE_RAZONABLE_FPS = 1.2

class DatosTiempo:
    """Agrupa varios datos relacionados con el tiempo"""
    fps: Final[int]
    datos_lag: Final[NumCicloToDatoLag]
    duracion_ultimo_ciclo: Milisegundos
    limite_razonable_por_frame: Final[Milisegundos]

    def __init__(self, fps: int):
        self.fps = fps
        self.datos_lag = {}
        self.limite_razonable_por_frame = self._get_limite_por_frame()

    def duracion_excesiva(self) -> bool:
        """Indica si la duracion del ultimo ciclo fue excesiva"""
        return self.duracion_ultimo_ciclo > self.limite_razonable_por_frame

    def registra_dato_lag(self, dato_lag: DatoLag) -> None:
        """Registra el DatoLag del ultimo ciclo"""
        num_ciclo = dato_lag.num_ciclo
        assert num_ciclo not in self.datos_lag
        self.datos_lag[num_ciclo] = dato_lag

    def _get_limite_por_frame(self) -> Milisegundos:
        limite_en_segundos = Segundos(COEFICIENTE_LIMITE_RAZONABLE_FPS / self.fps)
        return convertir_a_milisegundos(limite_en_segundos)
