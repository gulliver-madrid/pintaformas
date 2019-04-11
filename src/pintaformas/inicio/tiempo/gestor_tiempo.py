from typing import Final, Optional

from ...log_pintaformas import log
from ...core.general.medidor_tiempo import MedidorTiempo
from ..control_ciclos import ControlCiclos
from ...core.general.tiempo import Segundos, Milisegundos
from .control_tiempo import ControlTiempo
from .datos_tiempo import DatosTiempo
from .dato_lag import DatoLag



IMPRIMIR_TIEMPO_ACTUALIZACION_VISTA = True


DelayedMedidorTiempo = Optional[MedidorTiempo]


class GestorTiempo:
    '''Gestiona el tiempo a mas alto nivel que ControlTiempo'''
    _control_ciclos: Final[ControlCiclos]
    _control_tiempo: Final[ControlTiempo]
    _medidor_tiempo: DelayedMedidorTiempo
    data: Final[DatosTiempo]

    def __init__(self, control_ciclos: ControlCiclos, fps: int):
        self._control_ciclos = control_ciclos
        self._control_tiempo = ControlTiempo()
        self.data = DatosTiempo(fps)
        self._medidor_tiempo = None

    def establecer_medidor_tiempo(self, medidor_tiempo: MedidorTiempo) -> None:
        assert self._medidor_tiempo is None
        self._medidor_tiempo = medidor_tiempo

    def activar_reloj(self) -> None:
        self._control_tiempo.crear_reloj(self.data.fps)

    def ralentizar(self) -> None:
        '''
        Ralentiza el programa para ajustarse a las FPS y hace otras operaciones
        relacionadas
        '''
        self._tick_reloj()
        self._registrar_info_ciclo()

    def get_tiempo_actual(self) -> Segundos:
        return self._control_tiempo.tiempo_actual

    def imprimir_tiempo(self) -> None:
        return self._control_tiempo.imprimir_tiempo(self.data)


    def _tick_reloj(self) -> None:
        duracion_ciclo = self._control_tiempo.tick_reloj()
        self.data.duracion_ultimo_ciclo = duracion_ciclo

    def _registrar_info_ciclo(self) -> None:
        dato_lag = self._get_lag_ultimo_ciclo()
        self._log_tiempos(dato_lag)
        if self.data.duracion_excesiva():
            self.data.registra_dato_lag(dato_lag)

    def _get_lag_ultimo_ciclo(self) -> DatoLag:
        assert self._medidor_tiempo
        num_ciclo = self._control_ciclos.num_ciclo
        return DatoLag(
            num_ciclo=num_ciclo,
            total=self.data.duracion_ultimo_ciclo,
            vista=self._medidor_tiempo.tiempo_actualizacion_vista,
        )

    def _log_tiempos(self, dato_lag: DatoLag) -> None:
        """
        Loggea / imprime en pantalla informacion sobre los tiempos del ultimo ciclo
        """
        tiempo_vista_str = f'Tiempo actualizacion vista: {dato_lag.vista}'
        if IMPRIMIR_TIEMPO_ACTUALIZACION_VISTA:
            if dato_lag.vista > Milisegundos(5):
                print(tiempo_vista_str)
        log.anotar(f'Milisegundos desde ciclo anterior: {dato_lag.total}')
        log.anotar(tiempo_vista_str)
