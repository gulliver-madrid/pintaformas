from dataclasses import dataclass
from typing import TYPE_CHECKING, Final

from ...core.general.tiempo import Milisegundos

NumCiclo = int


@dataclass(init=False)
class DatoLag:
    """Representa los datos de lag de un ciclo concreto"""
    num_ciclo: Final[int]
    total: Final[Milisegundos]
    vista: Final[Milisegundos]

    def __init__(self, *, num_ciclo: NumCiclo, total: Milisegundos, vista: Milisegundos) -> None:
        self.num_ciclo = num_ciclo
        self.total = total
        self.vista = vista


if TYPE_CHECKING:
    d = DatoLag(num_ciclo=1, total=Milisegundos(200), vista=Milisegundos(100))

    # Errores esperados
    d.total = Milisegundos(3)  # type: ignore [misc] # No debe poderse asignar
