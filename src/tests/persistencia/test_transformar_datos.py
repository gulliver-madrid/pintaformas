# type: ignore # non-priority TODO

import unittest

from ...pintaformas.core.tipos import Color, PosicionEnDocumento
from ...pintaformas.core.elementos.formas import Linea, Circulo, Borrado
from ...pintaformas.core.persistencia.transformar_datos.transformar_datos import TransformarDatos

COLOR_LINEA = Color((200, 100, 0))
ORIGEN_LINEA = PosicionEnDocumento((200, 300))
DESTINO_LINEA = PosicionEnDocumento((250, 350))
POSICION_CIRCULO = PosicionEnDocumento((100, 100))
COLOR_CIRCULO = Color((0, 20, 40))
RADIO_CIRCULO = 25
OBJETOS = [
    Borrado(),
    Linea(ORIGEN_LINEA, DESTINO_LINEA, COLOR_LINEA),
    Circulo(COLOR_CIRCULO, POSICION_CIRCULO, RADIO_CIRCULO)
]
DATOS_NORMALIZADOS = [
    dict(
        tipo = 'borrado'
    ),
    dict(
        tipo = 'linea',
        color = COLOR_LINEA,
        origen = ORIGEN_LINEA,
        destino = DESTINO_LINEA,
    ),
    dict(
        tipo = 'circulo',
        posicion = POSICION_CIRCULO,
        color = COLOR_CIRCULO,
        radio = RADIO_CIRCULO,
    ),
]

class TestTransformarDatos(unittest.TestCase):

    def setUp(self):
        self.transformar_datos = TransformarDatos()

    def tearDown(self):
        pass

    @unittest.skip("Pendiente de analisis")
    def test_normalizar_datos(self):
        resultado = self.transformar_datos.normalizar_datos(OBJETOS)
        self.assertEqual(len(resultado), len(DATOS_NORMALIZADOS))
        for i, (dicc_obtenido, dicc_esperado) in enumerate(zip(resultado, DATOS_NORMALIZADOS)):
            with self.subTest(i=i, tipo_obtenido=dicc_obtenido['tipo']):
                self.assertEqual(dicc_obtenido, dicc_esperado)

    @unittest.skip("Pendiente de analisis")
    def test_convertir_datos_a_objetos(self):
        resultado = self.transformar_datos.convertir_datos_a_objetos(DATOS_NORMALIZADOS)
        self.assertEqual(len(resultado.historial), len(OBJETOS))
        for objeto_obtenido, objeto_esperado in zip(resultado.historial, OBJETOS):
            self.assertEqual(objeto_obtenido, objeto_esperado)


if __name__ == '__main__':
    unittest.main()
