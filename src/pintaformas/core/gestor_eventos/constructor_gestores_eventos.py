from typing import Type

from ..control_general.realizador import Realizador

from ..elementos.herramienta import Herramienta
from .gestor_eventos import KeyGestorEventos
from .bases.general import GestorDeEventosGeneral
from .universal.general import GestorDeEventosUniversal
from .circulo.general import GestorDeEventosSeleccionCirculo
from .normal.general import GestorDeEventosNormal
from .recta.general import GestorDeEventosRecta
from .flecha.general import GestorDeEventosFlecha
from .componentes import ComponentesGestoresEventos

DiccionarioDeClasesGestoresEventos = dict[KeyGestorEventos, Type[GestorDeEventosGeneral[Realizador]]]

clases_gestores_eventos: DiccionarioDeClasesGestoresEventos = {
    "universal" : GestorDeEventosUniversal,
    Herramienta.lapiz_libre : GestorDeEventosNormal,
    Herramienta.circulo : GestorDeEventosSeleccionCirculo,
    Herramienta.recta : GestorDeEventosRecta,
    Herramienta.seleccion : GestorDeEventosFlecha
}


class ConstructorGestoresEventos:
    def construir_gestores_eventos_generales(self, componentes: ComponentesGestoresEventos[Realizador]) -> dict[KeyGestorEventos, GestorDeEventosGeneral[Realizador]]:
        gestores_eventos = {}
        for nombre, clase in clases_gestores_eventos.items():
            try:
                gestor_eventos_general = clase(componentes)
            except BaseException as error:
                raise RuntimeError(f'Error tratando de crear el gestor eventos general {nombre!r}') from error
            gestores_eventos[nombre] = gestor_eventos_general
        return gestores_eventos
