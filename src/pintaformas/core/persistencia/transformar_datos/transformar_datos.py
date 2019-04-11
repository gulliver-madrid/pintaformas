from typing import Sequence
from .conversores import Recuperador
from .tipos import DatosNormalizadosUniversales
from .sistema_001 import RecuperadorSistema001
from .normalizador_sistema_002 import NormalizadorSistema002
from .recuperador_sistema_002 import RecuperadorSistema002
from .formatos_documento import DocumentoRecuperado

# TYPE_CHECKING
from ...general.doc_en_memoria import DocumentoEnMemoria
from ...elementos.forma import Forma

SISTEMA_ACTUAL_DE_CODIFICACION = '002'


class TransformarDatos:
    @staticmethod
    def normalizar_datos(documento: tuple[DocumentoEnMemoria, Sequence[Forma]]) -> dict[str, object]:
        '''Recibe la representacion de un documento y devuelve datos que puedan ser serializados con json'''
        assert len(documento) == 2, documento
        normalizador = NormalizadorSistema002()
        datos_normalizados = normalizador.normalizar_datos(documento)
        assert isinstance(datos_normalizados, dict)
        return datos_normalizados


    def convertir_datos_a_objetos(self, datos_normalizados: DatosNormalizadosUniversales) -> DocumentoRecuperado:
        '''Devuelve un documento adaptado al sistema_002'''
        assert isinstance(datos_normalizados, (list, dict))
        print(f'en TransformarDatos.convertir_datos_a_objetos, se recibe objeto: ({type(datos_normalizados).__name__})')
        sistema_codificacion = self.obtener_sistema_de_codificacion(datos_normalizados)
        print(f'en TransformarDatos.convertir_datos_a_objetos, se detecta que el sistema de codificacion es {sistema_codificacion}')

        recuperador: Recuperador
        if sistema_codificacion == '001':
            recuperador = RecuperadorSistema001()
        elif sistema_codificacion == '002':
            recuperador = RecuperadorSistema002()
        else:
            raise NotImplementedError(f'sistema de codificacion desconocido: {sistema_codificacion}')
        documento = recuperador.convertir_datos_a_documento(datos_normalizados)
        assert isinstance(documento, DocumentoRecuperado), f'{type(documento), sistema_codificacion}'
        print(f'en TransformarDatos.convertir_datos_a_objetos, el documento es del tipo {type(documento).__name__}')
        return documento


    def obtener_sistema_de_codificacion(self, datos_normalizados: DatosNormalizadosUniversales) -> str:
        if isinstance(datos_normalizados, list):
            # sistema antiguo, si es una lista es que es este
            return '001'
        elif isinstance(datos_normalizados, dict):
            # sistema moderno, usando un diccionario que informa del sistema de codificacion
            sistema_codificacion = datos_normalizados['codificacion']
            assert isinstance(sistema_codificacion, str)
            return sistema_codificacion
        else:
            raise TypeError(type(datos_normalizados))
