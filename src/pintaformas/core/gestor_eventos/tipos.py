from .bases.general import GestorDeEventosGeneral
from .bases.teclado import GestorEventosTecladoBase
from ..control_general.realizador import Realizador

# PF es por PintaFormas
GestorDeEventosPFGeneral = GestorDeEventosGeneral[Realizador]
GestorEventosPFTecladoBase = GestorEventosTecladoBase[Realizador]
