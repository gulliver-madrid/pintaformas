import unittest

from ...pintaformas.core.elementos.forma import Forma
from ...pintaformas.core.tipos.cev import CodigoForma


class TestForma(unittest.TestCase):
    def test_forma(self) -> None:
        Forma.num_forma = 0
        forma = Forma()
        self.assertEqual(forma.codigo, CodigoForma('forma_0001'))

if __name__ == '__main__':
    unittest.main()
