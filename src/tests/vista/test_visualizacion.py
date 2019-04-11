import unittest
from dataclasses import dataclass
from typing import Sequence
from ...pintaformas.core.vista.visualizacion import Visualizacion
from ...pintaformas.core.tipos import Tuple2Int, PosicionEnPantalla, PosicionEnDocumento

DIMS = X, Y = 0, 1

CENTRO_INICIAL = PosicionEnPantalla((2, 2))


@dataclass
class Datos:
    zoom: int
    punto_pivote: Tuple2Int
    posiciones_documento: Sequence[Tuple2Int]
    posiciones_pantalla: Sequence[Tuple2Int]


DATOS = [
    Datos(
        zoom=2,
        punto_pivote=(2, 2),
        posiciones_documento=[(2, 2), (2, 1), (3, 1), (3, 2)],
        posiciones_pantalla=[(2, 2), (2, 0), (4, 0), (4, 2)]
    ),
    Datos(
        zoom=1,
        punto_pivote=(3, 2),
        posiciones_documento=[(2, 2), (2, 1), (3, 1), (3, 2)],
        posiciones_pantalla=[(1, 2), (1, 1), (2, 1), (2, 2)]
    ),
    Datos(
        zoom=2,
        punto_pivote=(2, 1),
        posiciones_documento=[(2, 2), (2, 1), (3, 1), (3, 2)],
        posiciones_pantalla=[(2, 4), (2, 2), (4, 2), (4, 4)]
    ),
]


class TestZoomConDesplazamiento(unittest.TestCase):


    def test_zoom_con_desplazamiento(self) -> None:

        visualizacion = Visualizacion()
        visualizacion.centro_base = CENTRO_INICIAL
        for dato in DATOS:
            zoom = dato.zoom
            punto_pivote = dato.punto_pivote
            for dato_posicion_documento, esperada_pantalla in zip(dato.posiciones_documento, dato.posiciones_pantalla):
                posicion_documento = PosicionEnDocumento(dato_posicion_documento)
                with self.subTest(zoom=zoom, punto_pivote=punto_pivote, original=posicion_documento):
                    visualizacion.valor_zoom = zoom
                    visualizacion.punto_pivote = PosicionEnDocumento(punto_pivote)
                    resultado = visualizacion.pasar_a_pantalla(posicion_documento)
                    self.assertEqual(resultado, esperada_pantalla)


    def test_inversion_zoom_con_desplazamiento(self) -> None:

        visualizacion = Visualizacion()
        visualizacion.centro_base = CENTRO_INICIAL
        for dato in DATOS:
            zoom = dato.zoom
            punto_pivote = dato.punto_pivote

            for dato_posicion_pantalla, esperada_documento in zip(dato.posiciones_pantalla, dato.posiciones_documento):
                posicion_pantalla = PosicionEnPantalla(dato_posicion_pantalla)
                with self.subTest(zoom=zoom, punto_pivote=punto_pivote, original=posicion_pantalla):
                    visualizacion.valor_zoom = zoom
                    visualizacion.punto_pivote = PosicionEnDocumento(punto_pivote)
                    resultado = visualizacion.pasar_a_documento(posicion_pantalla)
                    self.assertEqual(resultado, esperada_documento)


if __name__ == '__main__':
    unittest.main()
