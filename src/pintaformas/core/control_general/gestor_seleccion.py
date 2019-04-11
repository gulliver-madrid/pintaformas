from ..tipos import Color, PosicionEnDocumento
from ..elementos.formas import Linea
from ..elementos.seleccion import Seleccion
from ..general.control_cambios import ControlDeCambios
from ..vista.vista import Vista
from ..vista.visualizacion import Visualizacion


class GestorSeleccion:
    __slots__ = ('visualizacion', 'color_pluma', 'seleccion', 'control_cambios')
    visualizacion: Visualizacion
    color_pluma: Color
    seleccion: Seleccion
    control_cambios: ControlDeCambios

    def __init__(self, seleccion: Seleccion, vista: Vista, control_cambios: ControlDeCambios):
        self.visualizacion = vista.visualizacion
        self.seleccion = seleccion
        self.control_cambios = control_cambios


    def _comprueba_nada_seleccionado(self) -> None:
        assert not self.seleccion.objeto_seleccionado, f'{self.seleccion.objeto_seleccionado}'


    def selecciona_linea_imaginaria(self, origen: PosicionEnDocumento, destino: PosicionEnDocumento) -> None:
        """Es una linea que aun no ha sido confirmada"""
        # self._comprueba_nada_seleccionado() # Parece innecesario
        self.seleccion.objeto_seleccionado = Linea(origen, destino, self.color_pluma)
        self.control_cambios.registrar(self.seleccion.codigo)

    def selecciona_linea(self, origen: PosicionEnDocumento, destino: PosicionEnDocumento) -> None:
        # self._comprueba_nada_seleccionado() # Parece innecesario
        self.seleccion.objeto_seleccionado = Linea(origen, destino, self.color_pluma)

    def deseleccionar(self) -> None:
        self.seleccion.objeto_seleccionado = None
