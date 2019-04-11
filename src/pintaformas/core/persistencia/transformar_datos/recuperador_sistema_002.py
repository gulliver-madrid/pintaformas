from ..transformar_datos.tipos import DatosNormalizadosDiccionario
from .conversores import Recuperador
from .tipos import DatosNormalizadosUniversales
from .sistema_001 import RecuperadorSistema001
from .formatos_documento import DocumentoRecuperado


CODIFICACION = '002'


class RecuperadorSistema002(Recuperador):

    def convertir_datos_a_documento(self, datos_normalizados: DatosNormalizadosUniversales) -> DocumentoRecuperado:
        assert isinstance(datos_normalizados, dict)
        return self._convertir_datos_a_documento(datos_normalizados)

    @staticmethod
    def _convertir_datos_a_documento(datos_normalizados: DatosNormalizadosDiccionario) -> DocumentoRecuperado:
        assert datos_normalizados['codificacion'] == CODIFICACION
        recuperador001 = RecuperadorSistema001()
        historial_normalizado = datos_normalizados['historial']
        capas_normalizado = datos_normalizados['capas']
        assert isinstance(capas_normalizado, list)
        capas = recuperador001.convertir_datos_a_objetos(capas_normalizado)
        return DocumentoRecuperado(list(capas))
