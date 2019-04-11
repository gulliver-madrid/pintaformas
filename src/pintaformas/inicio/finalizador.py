from dataclasses import dataclass, field
from typing import Optional

from ..log_pintaformas import log
from .control_ciclos import ControlCiclos
from .informe_performance import GestorInformePerformance
from .operaciones_eventos import PostprocesadorEventos
from .tiempo.gestor_tiempo import GestorTiempo

INFORME_PERFORMANCE_ACTIVO = False

@dataclass
class Finalizador:
    control_ciclos: ControlCiclos
    usar_persistencia: bool
    gestor_tiempo: GestorTiempo
    postprocesador_eventos: Optional[PostprocesadorEventos]
    gestor_informe_performance: Optional[GestorInformePerformance] = field(init=False)

    def __post_init__(self) -> None:
        self.gestor_informe_performance = GestorInformePerformance() if INFORME_PERFORMANCE_ACTIVO else None

    def procedimientos_finales(self) -> None:
        self.control_ciclos.detener()
        num_ciclos = self.control_ciclos.ciclos_totales
        print(f'Ciclos totales: {num_ciclos}')
        # Imprime en consola un mensaje de salida
        con_o_sin = 'con' if self.usar_persistencia else 'sin'
        print(f'Saliendo de la self.app {con_o_sin} persistencia')
        if self.gestor_informe_performance:
            self._mostrar_informe_performance()
        if (postprocesador := self.postprocesador_eventos) is not None:
            postprocesador.log_todos_los_eventos(num_ciclos)
            postprocesador.grabar_eventos_en_disco()
        # Muestra el tiempo en consola
        self.gestor_tiempo.imprimir_tiempo()
        log.imprimir_logs()

    def _mostrar_informe_performance(self) -> None:
        assert self.gestor_informe_performance
        self.gestor_informe_performance.mostrar_informe(
            self.control_ciclos.ciclos_totales,
            self.gestor_tiempo.data.datos_lag,
            self.gestor_tiempo.data.limite_razonable_por_frame
        )
