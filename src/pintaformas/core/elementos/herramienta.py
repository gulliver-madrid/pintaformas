from enum import auto

from ..dependencias import AutoName



class Herramienta(AutoName):
    seleccion = auto()
    lapiz_libre = auto()
    recta = auto()
    circulo = auto()


HERRAMIENTAS = [
    Herramienta.seleccion,
    Herramienta.lapiz_libre,
    Herramienta.recta,
    Herramienta.circulo,
]
