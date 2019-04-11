from .gestor_eventos import GestorDeEventos
from .constructor_gestores_eventos import ConstructorGestoresEventos
from .componentes import ComponentesGestoresEventos
from .modos import Modos


# TYPE_CHECKING:
from ...dependencias import PygameEvent
from ..control_general.realizador import Realizador
from ..general.observador_herramienta import EstadoHerramientaObservado

def crear_gestor_eventos(
        realizador: Realizador,
        estado_herramienta: EstadoHerramientaObservado
        ) -> GestorDeEventos:

    modos = Modos()

    componentes_gestores_especificos = ComponentesGestoresEventos(
        realizador=realizador,
        modos=modos,
    )

    constructor_gestores_eventos = ConstructorGestoresEventos()
    gestores_eventos_generales = \
        constructor_gestores_eventos.construir_gestores_eventos_generales(componentes_gestores_especificos)

    return GestorDeEventos(realizador, modos, gestores_eventos_generales, estado_herramienta)
