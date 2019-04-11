from ..tipos import PosicionEnDocumento, Dimensiones, Color, CodigoObjetoEspecial
from ..objetos import ObjetoVectorial
from .. import cfg


class Lienzo(ObjetoVectorial):
    tipo = 'lienzo'

    def __init__(self) -> None:
        self.codigo = CodigoObjetoEspecial.lienzo
        self.posicion = PosicionEnDocumento((0, 0))
        self.color = Color((255, 255, 255))
        self.dimensiones_lienzo = Dimensiones(cfg.DIMENSIONES_LIENZO)
        # print(f'Lienzo: creado lienzo con dimensiones {self.dimensiones_lienzo}')
        super().__init__()
