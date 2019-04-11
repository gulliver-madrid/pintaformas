
from dataclasses import dataclass
from enum import auto
from typing import NewType, Sequence, Union

from ..dependencias import AutoName

@dataclass(frozen=True)
class CodigoElementoVistaStr:
    cadena: str


class CodigoElementoVistaEnum(AutoName):
    pass


CodigoElementoVista = Union[CodigoElementoVistaStr, CodigoElementoVistaEnum]



class CodigoForma(CodigoElementoVistaStr):
    pass


class CodigoObjetoEspecial(CodigoElementoVistaEnum):
    seleccion = auto()
    cursor = auto()
    dibujo = auto()
    lienzo = auto()
    visualizacion = auto()


LIENZO_DIBUJO_SELECCION: Sequence[CodigoObjetoEspecial] = (
    CodigoObjetoEspecial.lienzo,
    CodigoObjetoEspecial.dibujo,
    CodigoObjetoEspecial.seleccion
)

CodigoStr = NewType('CodigoStr', str)


def codigo_to_string(codigo: CodigoElementoVista) -> CodigoStr:
    if isinstance(codigo, CodigoElementoVistaStr):
        return CodigoStr(codigo.cadena)
    assert isinstance(codigo, CodigoElementoVistaEnum)
    assert isinstance(codigo.value, str), codigo.value
    return CodigoStr(codigo.value)


class CodigoArea(CodigoElementoVistaEnum):
    pass

# Especificos PintaFormas


class CodigoAreaPF(CodigoArea):
    area_dibujo = auto()
    area_color_seleccionado = auto()
    area_muestras_colores = auto()
    area_informativa = auto()
    area_herramientas = auto()
