from typing import NoReturn

from ..excepciones_eventos import EventoUsado
from ..tipos import GestorEventosPFTecladoBase

class GestorEventosTecladoRecta(GestorEventosPFTecladoBase):
    '''
    Gestiona los eventos del teclado cuando esta activada la herramienta 'recta'
    '''

    def init(self) -> None:
        self.equivalencias = {
            's': self.abandonar_recta,
        }

    def abandonar_recta(self) -> NoReturn:
        self.realizador.abandonar_recta()
        raise EventoUsado()
