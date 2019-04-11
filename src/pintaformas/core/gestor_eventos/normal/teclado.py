from ..tipos import GestorEventosPFTecladoBase

class GestorEventosTecladoNormal(GestorEventosPFTecladoBase):
    '''
    Gestiona los eventos del teclado cuando esta activada la herramienta 'lapiz_libre'
    '''

    def init(self) -> None:

        self.equivalencias = {
        }
