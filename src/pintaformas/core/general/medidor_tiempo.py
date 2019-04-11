from enum import auto
from typing import  Optional

from ..dependencias import AutoName
from .tiempo import Milisegundos, convertir_a_milisegundos, Timer

class SituacionMedidorTiempo(AutoName):
    INICIO_ACTUALIZACION_VISTA=auto()
    FIN_ACTUALIZACION_VISTA=auto()


class MedidorTiempo:
    tiempo_actualizacion_vista: Milisegundos
    _timer: Optional[Timer]=None

    def registrar(self, situacion: SituacionMedidorTiempo) -> None:
        if situacion == SituacionMedidorTiempo.INICIO_ACTUALIZACION_VISTA:
            self._timer = Timer()
        elif situacion == SituacionMedidorTiempo.FIN_ACTUALIZACION_VISTA:
            timer = self._timer
            assert timer, timer
            self.tiempo_actualizacion_vista = convertir_a_milisegundos(timer.info())
            self._timer=None
