import unittest

from ....pintaformas.core.gestor_eventos.modos import Modos


class TestModos(unittest.TestCase):
    def test_modos_establecer_y_obtener_valor(self) -> None:
        modos = Modos()
        self.assertEqual(modos.obtener_valor('control'), False)
        modos.establecer('control', True)
        self.assertEqual(modos.obtener_valor('control'), True)

    def test_modos_alguno_activado(self) -> None:
        modos = Modos()
        self.assertEqual(modos.alguno_activado, False)
        modos.establecer('control', True)
        self.assertEqual(modos.alguno_activado, True)



if __name__ == '__main__':
    unittest.main()
