
from ..tipos import Color, PosicionEnDocumento
from .. import cfg
from .forma import Forma

COLOR_POR_DEFECTO = cfg.COLOR_PLUMA
GROSOR_LINEA = 5


class Circulo(Forma):
    tipo = 'circulo'
    atributos_eq = ['posicion', 'color', 'radio']

    def __init__(self, color: Color, posicion: PosicionEnDocumento, radio: int):
        assert radio > 0
        self.posicion = posicion
        self.color = color
        self.radio = radio
        super().__init__()



class Linea(Forma):
    tipo = 'linea'
    atributos_eq = ['origen', 'destino', 'color', 'grosor']

    def __init__(self, origen: PosicionEnDocumento, destino: PosicionEnDocumento, color: Color):
        self.origen = origen
        self.destino = destino
        self.color = color
        self.grosor = GROSOR_LINEA
        super().__init__()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.origen}, {self.destino})'


class Borrado(Forma):
    '''Representa un borrado del area de dibujo'''
    tipo = 'borrado'


BORRADO = Borrado()
