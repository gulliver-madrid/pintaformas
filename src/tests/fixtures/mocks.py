from unittest.mock import MagicMock
from typing import cast

from ...pintaformas.core.control_general.estado_herramienta import EstadoHerramienta
from ...pintaformas.core.control_general.control_general import ControlGeneral
from ...pintaformas.core.vista.vista import Vista



def crear_mock_control_general() -> ControlGeneral:
    return cast(ControlGeneral, MagicMock())

def crear_mock_vista() -> Vista:
    return cast(Vista, MagicMock())

def crear_mock_estado_herramienta() -> EstadoHerramienta:
    return cast(EstadoHerramienta, MagicMock())
