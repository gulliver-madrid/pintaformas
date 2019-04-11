from typing import Literal, Set

from ...log_pintaformas import log

from ..objetos.objeto import Objeto

Modo = Literal['boton_pulsado', 'control', 'shift']

class Modos(Objeto):
    """Durante la ejecucion del programa se crea un unico objeto Modos, cuyo estado se establece desde el GestorDeEventosBase, y se lee desde los gestores de eventos de teclado."""
    data: dict[Modo, bool]
    def __init__(self) -> None:
        self.data = {'boton_pulsado': False, 'control': False, 'shift': False}

    @property
    def activados(self) -> Set[str]:
        return set(modo for modo, valor in self.data.items() if valor)

    def establecer(self, nombre: Modo, valor: bool) -> None:
        if nombre not in self.data.keys():
            raise ValueError(nombre)
        self.data[nombre] = valor
        log.anotar(f'Modos activados: {self.activados}')


    def obtener_valor(self, nombre: Modo) -> bool:
        return self.data[nombre]

    @property
    def alguno_activado(self) -> bool:
        return any(modo for modo in self.data.values())
