
class ControlCiclos:
    def __init__(self) -> None:
        self.num_ciclo = 0
        self.ciclos_totales = 0

    def detener(self) -> None:
        self.ciclos_totales = self.num_ciclo
