import pygame
from ...dependencias import PygameClock
from ...core.general.tiempo import Timer, convertir_a_milisegundos, Segundos, Milisegundos
from .datos_tiempo import DatosTiempo


class ControlTiempo:
    tiempo_setup_y_primer_ciclo: Milisegundos
    tiempo_total: Milisegundos
    fps: int
    reloj: PygameClock

    def __init__(self) -> None:
        self.tiempo_setup_y_primer_ciclo = Milisegundos(0)  # mide el tiempo hasta el primer tick del reloj
        self.timer = Timer()
        self.tiempo_total = Milisegundos(0)

    def crear_reloj(self, fps: int) -> None:
        self.reloj = pygame.time.Clock()
        self.fps = fps

    def imprimir_tiempo(self, datos_tiempo: DatosTiempo) -> None:
        print(f'Tiempo de inicio: {int(self.tiempo_setup_y_primer_ciclo)} milisegundos')
        print(f'Tiempo actual: {int(convertir_a_milisegundos(self.tiempo_actual))} milisegundos')
        print(f'Tiempo total: {int(self.tiempo_total)} milisegundos')
        tiempo_total_vista = sum((dato.vista for dato in datos_tiempo.datos_lag.values()), start=Milisegundos(0))
        print(f'Tiempo total vista: {tiempo_total_vista}')

    @property
    def tiempo_actual(self) -> Segundos:
        return Segundos(self.timer.info())

    def tick_reloj(self) -> Milisegundos:
        if not self.tiempo_total:
            # primer ciclo
            print('Inicializando el tiempo en ControlTiempo')
            self.tiempo_setup_y_primer_ciclo = convertir_a_milisegundos(self.timer.info())
            assert type(self.tiempo_total) == type(self.tiempo_setup_y_primer_ciclo)
            self.tiempo_total = Milisegundos(self.tiempo_total + self.tiempo_setup_y_primer_ciclo)

        milisegundos = Milisegundos(self.reloj.tick(self.fps))
        assert type(self.tiempo_total) == type(milisegundos)
        self.tiempo_total = Milisegundos(self.tiempo_total + milisegundos)
        return milisegundos
