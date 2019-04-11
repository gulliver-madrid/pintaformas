import math

from ...tipos import Posicion, PosicionEnPantalla, Dimensiones

DIMS = X, Y = 0, 1

class Reposicionador:
    '''Calcula los datos para crear una capa que comprenda una linea, en vez
    de pintar la linea directamente'''

    def hallar_posicion_y_dimensiones_capa(self,
            origen: PosicionEnPantalla,
            destino: PosicionEnPantalla,
            grosor: int,
            dim_maximas: Dimensiones
            ) -> tuple[PosicionEnPantalla, Dimensiones, PosicionEnPantalla, PosicionEnPantalla]:

        largo_linea_original = self.calcular_largo_linea(origen, destino)

        margen = (grosor // 2) + 1
        dim_rect_linea = Dimensiones(abs(destino.restar(origen)))

        if origen[X] <= destino[X]:
            # de izquierda a derecha
            if origen[Y] <= destino[Y]:
                # de arriba a abajo (linea descendente)
                punto_sup_izq = origen
            else:
                # de abajo a arriba (linea ascendente)
                punto_sup_izq = PosicionEnPantalla((origen[X], destino[Y]))

        else:
            # de derecha a izquierda
            if origen[Y] <= destino[Y]:
                # de arriba a abajo (linea ascendente inversa)
                punto_sup_izq = PosicionEnPantalla((destino[X], origen[Y]))
            else:
                # de abajo a arriba (linea descendente inversa)
                punto_sup_izq = destino

        posicion_capa = punto_sup_izq.restar_entero(margen)
        origen_interno = origen.restar(posicion_capa)
        destino_interno = destino.restar(posicion_capa)

        largo_linea = self.calcular_largo_linea(origen_interno, destino_interno)
        assert largo_linea == largo_linea_original

        dimensiones_capa = dim_rect_linea.sumar_entero(2 * margen)

        if any(dimensiones_capa[dim] > dim_maximas[dim] for dim in DIMS):
            dimensiones_capa = dim_maximas
            # print(f'dimensiones_capa: {dimensiones_capa}')
        return posicion_capa, dimensiones_capa, origen_interno, destino_interno


    @staticmethod
    def calcular_largo_linea(origen: Posicion, destino: Posicion) -> int:
        largo_linea = round(math.sqrt((destino[X] - origen[X]) ** 2 + (destino[Y] - origen[Y]) ** 2))
        return largo_linea
