import unittest
from unittest.mock import MagicMock

from ....pintaformas.core.tipos import Color
from ....pintaformas.core.control_general.control_general import ControlGeneral
from ....pintaformas.core.control_general.realizador import Realizador
from ....pintaformas.core.control_general.gestor_seleccion import GestorSeleccion
from ....pintaformas.core.control_general.variables_estado import VariableDeEstado


class TestRealizadorSeleccionarColor(unittest.TestCase):
    '''
    Comprueba la correcta comunicacion entre el Realizador y el AreaMuestrasColores
    para que se muestre el color seleccionado
    '''
    def setUp(self) -> None:
        self.vista = MagicMock()
        gestor_cursor = MagicMock()
        color_seleccionado = VariableDeEstado()
        control_cambios= MagicMock()
        estado= MagicMock()
        self.gestor_seleccion = GestorSeleccion(self.vista, estado, control_cambios)
        control_general = ControlGeneral(
            gestor_cursor = gestor_cursor,
            gestor_seleccion=self.gestor_seleccion, gestor_seleccion_circulo=MagicMock(),dibujador_en_documento=MagicMock(),vista=self.vista
            )
        self.realizador = Realizador(control_general, control_cambios, MagicMock())
        self.vista.areas.color_seleccionado.set_color_seleccionado = MagicMock()


    def test_realizador_seleccionar_color(self) -> None:
        '''realizador.seleccionar_color modifica el color_seleccionado y la muestra visible en area_muestras_colores'''
        COLOR_A_SELECCIONAR = Color((50, 50, 50))
        self.realizador.seleccionar_color(COLOR_A_SELECCIONAR)
        self.assertEqual(self.gestor_seleccion.color_pluma, COLOR_A_SELECCIONAR)
        self.assertEqual(self.vista.areas.color_seleccionado.color_seleccionado, COLOR_A_SELECCIONAR)






if __name__ == '__main__':
    unittest.main()
