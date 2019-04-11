from ..core.general.tiempo import Milisegundos
from .tiempo import DatoLag, NumCicloToDatoLag

MARGEN = ' ' * 2


class GestorInformePerformance:

    def mostrar_informe(self, ciclos_totales: int, ms_por_frame_excesivos: NumCicloToDatoLag, limite: Milisegundos) -> None:
        self._anotar(ciclos_totales, ms_por_frame_excesivos, limite)

    def _anotar(self, ciclos_totales: int, ms_por_frame_excesivos: NumCicloToDatoLag, limite: Milisegundos) -> None:
        self._imprimir('\nInforme sobre performance:')
        self._imprimir(f'Ciclos totales: {ciclos_totales}', 1)
        if ms_por_frame_excesivos:
            self._imprimir(f'FPS excesivos (milisegundos > {limite}):', 1)
            for num_ciclo, dato_lag in ms_por_frame_excesivos.items():
                self._imprimir_info_ciclo(num_ciclo, dato_lag)
        else:
            self._imprimir(f'No hubo FPS excesivos', 1)
        print()


    def _imprimir_info_ciclo(self, num_ciclo: int, dato_lag: DatoLag) -> None:
        duracion_ultimo_ciclo = dato_lag.total
        tiempo_vista = dato_lag.vista
        info_ciclo = f'Ciclo: {num_ciclo:4d} Tiempo: {duracion_ultimo_ciclo:4d}, del cual vista: {tiempo_vista:4d}'
        self._imprimir(info_ciclo, 2)

    def _imprimir(self, texto: str, num_margenes: int = 0) -> None:
        print(f'{MARGEN * num_margenes}{texto}')
