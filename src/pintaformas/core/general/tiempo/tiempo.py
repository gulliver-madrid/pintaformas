import time

class Milisegundos(float):
    nombre = 'milisegundos'

class Segundos(float):
    nombre = 'segundos'


class Timer:
    tiempo_inicial:Segundos
    def __init__(self) -> None:
        self.tiempo_inicial = Segundos(time.time())

    def info(self) -> Segundos:
        return Segundos(time.time() - self.tiempo_inicial)


def convertir_a_milisegundos(tiempo_en_segundos: Segundos) -> Milisegundos:
    return Milisegundos(int(tiempo_en_segundos * 1000))
