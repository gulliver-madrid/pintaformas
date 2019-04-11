from ..observador import Observador
from ..elementos.herramienta import Herramienta
from ..control_general.estado_herramienta import EstadoHerramienta

class EstadoHerramientaObservado(Observador):
    valor: Herramienta
    def __init__(self, _objeto: EstadoHerramienta):
        super().__init__(_objeto)
