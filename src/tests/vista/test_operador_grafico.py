import unittest

from ...pintaformas.core.vista.surfaces import PygameSurfaceWrapperFactory
from ...pintaformas.core.vista.operador_grafico import OperadorGrafico


class TestOperadorGrafico(unittest.TestCase):

    def test_test_operador_grafico_crear_surface(self) -> None:
        operador_grafico = OperadorGrafico(PygameSurfaceWrapperFactory())
        surface = operador_grafico.crear_surface((20, 20))
        self.assertTrue(surface)


if __name__ == '__main__':
    unittest.main()
