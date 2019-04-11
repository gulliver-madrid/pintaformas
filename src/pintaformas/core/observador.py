from copy import deepcopy
from .tipos.transformar import obtener_atributo

class Observador:
    # TODO: Convertir en generico
    def __init__(self, _objeto: object) -> None:
        self._objeto = _objeto

    def __getattr__(self, nombre: str) -> object:
        valor = obtener_atributo(self._objeto, nombre)
        return deepcopy(valor)
