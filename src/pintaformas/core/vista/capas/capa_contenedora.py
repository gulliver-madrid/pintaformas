from ...tipos.cev import CodigoElementoVista
from ...tipos import Dimensiones
from .capa import Capa



class CapaContenedora(Capa):

    __slots__ = ('dimensiones', 'capas_internas')
    capas_internas: list[Capa]
    dimensiones: Dimensiones

    tipo_de_capa = 'contenedora'

    def __init__(self, codigo: CodigoElementoVista):
        self.dimensiones: Dimensiones
        self.capas_internas: list[Capa] = []
        super().__init__(codigo)

    def anadir_capa(self, capa: Capa) -> None:
        self.capas_internas.append(capa)

    def set_dimensiones(self, dimensiones: Dimensiones) -> None:
        self.dimensiones = dimensiones
