
from .conversores import Normalizador

# TYPE_CHECKING
from typing import Sequence, Union, cast
from ...tipos.transformar import obtener_atributo
from .tipos import DiccionarioStrObject, DatosNormalizadosLista
from ...general.doc_en_memoria import DocumentoEnMemoria
from ...elementos.forma import Forma

CODIFICACION = '002'

ATRIBUTOS_POR_TIPO: dict[str, list[str]] = dict(
    linea=['origen', 'destino'],
    circulo=['posicion', 'color', 'radio'],
    borrado=[],
)


class NormalizadorSistema002(Normalizador):

    def normalizar_datos(self, documento_base: tuple[DocumentoEnMemoria, Sequence[Forma]]) -> DiccionarioStrObject:
        # print(__file__, f"{documento_base=}")
        assert len(documento_base) == 2, documento_base

        historial, capas = documento_base

        historial_normalizado = self._normalizar_datos(historial)
        capas_normalizado = self._normalizar_datos(capas)
        datos_normalizados = dict(
            codificacion=CODIFICACION,
            historial=historial_normalizado,
            capas=capas_normalizado,
        )
        return cast(DiccionarioStrObject, datos_normalizados)

    @staticmethod
    def _normalizar_datos(documento: Union[DocumentoEnMemoria, Sequence[Forma]]) -> DatosNormalizadosLista:
        '''Recibe el historial en formato lista de objetos customizados y devuelve una lista
        de diccionarios'''
        # print(f'sistema_001.normalizar_datos({type(documento)})')
        datos_normalizados: list[DiccionarioStrObject] = []
        for objeto in documento:
            assert isinstance(objeto, Forma)
            if objeto.tipo in ATRIBUTOS_POR_TIPO:
                # reveal_type(ATRIBUTOS_POR_TIPO)
                atributos = ATRIBUTOS_POR_TIPO[objeto.tipo]
                if objeto.tipo == 'linea' and 'color' not in atributos:
                    atributos.append('color')
            else:
                raise ValueError(objeto)
            dato_normalizado = {}
            for nombre in ['tipo'] + atributos:
                valor = obtener_atributo(objeto, nombre)
                assert isinstance(valor, object)
                # print('en sistema_001.normalizar_datos, valor:', type(valor))
                dato_normalizado[nombre] = valor

            datos_normalizados.append(dato_normalizado)
        return datos_normalizados
