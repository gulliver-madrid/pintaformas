import unittest
from .. import ajustar_texto

TEXTO = "____Modo normal____\nPara hacer un trazo, manten pulsado el raton mientras lo desplazas.\nPara entrar en modo seleccion_circulo, pulsa 'c'\nPara borrar la pantalla, pulsa 'b'\nPara resetear, pulsa 'r'\n"
AJUSTE = 50
RESULTADO_ESPERADO = [
"____Modo normal____",
"Para hacer un trazo, manten pulsado el raton mient", # 50 caracteres
"ras lo desplazas.",
"Para entrar en modo seleccion_circulo, pulsa 'c'",
"Para borrar la pantalla, pulsa 'b'",
"Para resetear, pulsa 'r'"
]
class TestPrepararTexto(unittest.TestCase):

    def setUp(self) -> None:
        self.preparar_texto_para_renderizar = ajustar_texto.preparar_texto_para_renderizar

    def tearDown(self) -> None:
        pass

    def test_preparar_texto_para_renderizar(self) -> None:
        resultado = self.preparar_texto_para_renderizar(TEXTO, AJUSTE)
        self.assertEqual(resultado, RESULTADO_ESPERADO)


if __name__ == '__main__':
    unittest.main()
