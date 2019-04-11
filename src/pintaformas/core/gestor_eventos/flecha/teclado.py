from ..tipos import GestorEventosPFTecladoBase


class GestorEventosTecladoFlecha(GestorEventosPFTecladoBase):
    '''
    Gestiona los eventos del teclado cuando esta activada la herramienta 'seleccion'
    '''

    def init(self) -> None:

        self.equivalencias = {
            'backspace': self.realizador.borrar_capa_seleccionada,
        }
