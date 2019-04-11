from ..tipos import GestorEventosPFTecladoBase

class GestorEventosTecladoSeleccionCirculo(GestorEventosPFTecladoBase):
    '''
    Gestiona los eventos del teclado cuando esta activada la herramienta 'circulo'
    '''

    def init(self) -> None:
        self.equivalencias  = {
        }

    def accion_flecha(self, direccion: str) -> None:
        self.realizador.modificar_circulo_seleccionado(direccion)
