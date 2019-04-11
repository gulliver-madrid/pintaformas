from dataclasses import dataclass

from ..vista.vista import Vista
from .dibujador_en_documento import DibujadorEnDocumento
from .gestor_cursor import GestorCursor
from .gestor_seleccion import GestorSeleccion
from .gestor_seleccion_circulo import GestorSeleccionCirculo


@dataclass
class ControlGeneral:
    __slots__ = ('gestor_cursor', 'gestor_seleccion', 'gestor_seleccion_circulo', 'dibujador_en_documento', 'vista')
    gestor_cursor: GestorCursor
    gestor_seleccion: GestorSeleccion
    gestor_seleccion_circulo: GestorSeleccionCirculo
    dibujador_en_documento: DibujadorEnDocumento
    vista: Vista
