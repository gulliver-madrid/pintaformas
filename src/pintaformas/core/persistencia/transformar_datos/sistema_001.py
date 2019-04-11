from typing import Sequence, cast

from ..transformar_datos.tipos import DatosNormalizadosLista
from ...tipos import Color, PosicionEnDocumento, Tuple2Int, convertir_a_tupla_tres_int
from ...elementos.formas import Linea, Circulo, Borrado
from ...elementos.forma import Forma
from .formatos_documento import DocumentoRecuperado
from .conversores import Recuperador
from .tipos import DatosNormalizadosUniversales


CLASES = dict(
    linea=Linea,
    circulo=Circulo,
    borrado=Borrado,
)


class RecuperadorSistema001(Recuperador):
    def convertir_datos_a_documento(self, datos_normalizados: DatosNormalizadosUniversales) -> DocumentoRecuperado:
        assert isinstance(datos_normalizados, list)
        return self._convertir_datos_a_documento(datos_normalizados)

    def _convertir_datos_a_documento(self, datos_normalizados: DatosNormalizadosLista) -> DocumentoRecuperado:
        preformas = self.convertir_datos_a_objetos(datos_normalizados)
        formas: list[Forma] = []
        for forma in preformas:
            if forma.tipo == 'borrado':
                formas.clear()
            else:
                formas.append(forma)
        return DocumentoRecuperado(formas)

    @staticmethod
    def convertir_datos_a_objetos(datos_normalizados: DatosNormalizadosLista) -> Sequence[Forma]:
        '''Los DatosNormalizados siempre estan en formato json'''
        objetos = []
        objeto: Forma
        for dato in datos_normalizados:
            tipo = dato['tipo']
            assert isinstance(tipo, str)
            if tipo in CLASES:
                Clase = CLASES[tipo]
                kwargs = {nombre: valor for nombre, valor in dato.items()}
                del kwargs['tipo']
                if tipo == 'linea':
                    if 'color' in dato.keys():
                        _color = dato['color']
                        assert isinstance(_color, list), _color
                        color = Color(convertir_a_tupla_tres_int(_color))
                    else:
                        color = Color((0, 0, 0))

                    origen = convertir_tupla2int_a_posicion(kwargs['origen'])
                    destino = convertir_tupla2int_a_posicion(kwargs['destino'])
                    objeto = Linea(origen, destino, color)
                elif tipo == 'circulo':
                    dato_color = kwargs['color']
                    assert isinstance(dato_color, list)
                    color = Color(convertir_a_tupla_tres_int(dato_color))
                    posicion = convertir_tupla2int_a_posicion(kwargs['posicion'])
                    radio = kwargs['radio']
                    assert isinstance(radio, int)
                    objeto = Circulo(color, posicion, radio)
                else:
                    objeto = Clase(**kwargs)
                assert isinstance(objeto, Forma)
            else:
                raise ValueError(dato)

            objetos.append(objeto)
        return objetos


def convertir_tupla2int_a_posicion(posicion: object) -> PosicionEnDocumento:
    assert isinstance(posicion, list), posicion
    assert len(posicion) == 2
    tupla_posicion = cast(Tuple2Int, posicion)
    return PosicionEnDocumento(tupla_posicion)
