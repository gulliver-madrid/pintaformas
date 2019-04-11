from typing import TypeVar

from ..tipos import (Posicion, PosicionEnDocumento, PosicionEnPantalla,
                     TuplaDosEnteros, Tuple2Int, Vector2D)

ZOOM_INICIAL = 2
PIVOTE_INICIAL = (0, 0)

DIMS = 0, 1
PADDING = (20, 20)


_Int_or_Tuple2Int = TypeVar('_Int_or_Tuple2Int', Tuple2Int, int)


class Visualizacion:
    def __init__(self) -> None:
        self.valor_zoom: float = ZOOM_INICIAL
        self.codigo = 'visualizacion'
        self.punto_pivote: PosicionEnDocumento
        self.centro_base: PosicionEnPantalla

    def establecer_centro_base(self, centro_doc: PosicionEnPantalla) -> None:
        self.centro_base = centro_doc.sumar(PADDING)
        self.punto_pivote = PosicionEnDocumento(round(centro_doc[dim] / self.valor_zoom) for dim in DIMS)


    def pasar_a_pantalla(self, posicion: PosicionEnDocumento) -> PosicionEnPantalla:
        assert isinstance(posicion, PosicionEnDocumento)
        posicion_relativa = posicion.restar(self.punto_pivote)
        posicion_relativa_con_zoom = self.aplicar_zoom(posicion_relativa)
        return self.centro_base.sumar(posicion_relativa_con_zoom)


    # DOS OPCIONES para este metodo y el de arriba (pasar_a_pantalla): dejarlos asi o aplicarlo como abajo
    # def pasar_a_documento(self, posicion: PosicionEnPantalla) -> PosicionEnDocumento:
    #     posicion_relativa = posicion.restar(self.centro_base)
    #     posicion_relativa_sin_zoom = self.aplicar_zoom(posicion_relativa, False)
    #     return self.punto_pivote.sumar(posicion_relativa_sin_zoom)


    def pasar_a_documento(self, posicion: PosicionEnPantalla) -> PosicionEnDocumento:
        nueva_posicion = self.cambiar_coordenadas(posicion, self.centro_base, self.punto_pivote, zoom_inverso=True)
        assert isinstance(nueva_posicion, PosicionEnDocumento)
        return nueva_posicion

    def cambiar_coordenadas(self, posicion: Posicion, centro_original: Posicion, nuevo_centro: Posicion, *, zoom_inverso: bool = False) -> Posicion:
        relativa = posicion.restar(centro_original)
        relativa_cambio_escala = self.aplicar_zoom(relativa, inverso=zoom_inverso)
        return nuevo_centro.sumar(relativa_cambio_escala)


    def desplazar(self, desplazamiento: Vector2D) -> None:
        desplazamiento_cambio_escala = Vector2D(self.aplicar_zoom(desplazamiento, inverso=True))
        self.punto_pivote = self.punto_pivote.sumar(desplazamiento_cambio_escala)


    def aplicar_zoom(self, target: _Int_or_Tuple2Int, *, inverso: bool = False) -> _Int_or_Tuple2Int:
        '''
            valor = True: Se aplica el zoom al target
            valor = False: el target ya tiene el zoom aplicado; lo desaplicamos
        '''

        assert isinstance(target, (tuple, list, int)), f'target: {target}'
        valor_zoom = (1 / self.valor_zoom) if inverso else self.valor_zoom
        return _aplicar_zoom_directo(target, valor_zoom)


# Funciones independientes

def _aplicar_zoom_directo(target: _Int_or_Tuple2Int, valor_zoom_a_aplicar: float) -> _Int_or_Tuple2Int:
    '''Aplica el zoom a un entero o a una tupla de dos enteros'''
    if isinstance(target, tuple):
        assert len(target) == 2
        return TuplaDosEnteros(_aplicar_zoom_directo(target[dim], valor_zoom_a_aplicar) for dim in DIMS)
    else:
        assert isinstance(target, int), f'{target}'
        return round(target * valor_zoom_a_aplicar)
