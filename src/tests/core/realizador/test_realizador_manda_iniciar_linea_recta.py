import unittest
from unittest.mock import MagicMock

from ....pintaformas.core.control_general.control_general import ControlGeneral
from ....pintaformas.core.control_general.gestor_seleccion import GestorSeleccion
from ....pintaformas.core.elementos.seleccion import Seleccion
from ....pintaformas.core.tipos import PosicionEnPantalla
from ....pintaformas.core.control_general.realizador import Realizador


class TestRealizador(unittest.TestCase):

    def setUp(self) -> None:
        gestor_seleccion = GestorSeleccion(Seleccion(), MagicMock(), MagicMock())
        control_general = ControlGeneral(MagicMock(), gestor_seleccion, MagicMock(), MagicMock(), MagicMock(),)
        self.realizador = Realizador(control_general, MagicMock(), MagicMock())
        self.realizador.establece_valores_iniciales()


    def test_realizador_manda_iniciar_trazo(self) -> None:
        origen = PosicionEnPantalla((20, 20))
        self.realizador.lapiz.iniciar_trazo(origen)
        assert(self.realizador.lapiz.trazo_iniciado)
        self.assertEqual(self.realizador.lapiz.trazo_iniciado.origen, origen)

    def test_realizador_manda_finalizar_trazo(self) -> None:
        origen = PosicionEnPantalla((20, 20))
        fin = PosicionEnPantalla((30, 30))
        self.realizador.lapiz.iniciar_trazo(origen)
        self.realizador.lapiz.finalizar_trazo(fin)
        self.assertEqual(self.realizador.lapiz.trazo_iniciado, None)


if __name__ == '__main__':
    unittest.main()
