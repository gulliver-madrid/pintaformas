import unittest
from .. import ajustar_texto

TEXTO = "Para hacer un trazo, manten pulsado el raton mientras lo desplazas."
AJUSTE = 50
RESULTADO_ESPERADO = [
    "Para hacer un trazo, manten pulsado el raton mient", # 50 caracteres
    "ras lo desplazas."]

class TestAjustarTexto(unittest.TestCase):

    def setUp(self) -> None:
        self.ajustar_texto = ajustar_texto.ajustar_texto

    def tearDown(self) -> None:
        pass

    def test_ajustar_texto(self) -> None:
        resultado = self.ajustar_texto(TEXTO, AJUSTE)
        self.assertEqual(resultado, RESULTADO_ESPERADO)


if __name__ == '__main__':
    unittest.main()
