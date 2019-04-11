
# TYPE_CHECKING
from ...elementos.forma import Forma
from ...general.doc_en_memoria import DocumentoEnMemoria
from .formatos_documento import DocumentoRecuperado
from .tipos import DiccionarioStrObject, \
    DatosNormalizadosUniversales



class Normalizador:
    def normalizar_datos(self, documento_base: tuple[DocumentoEnMemoria, list[Forma]]) -> DiccionarioStrObject:
        ...

class Recuperador:
    def convertir_datos_a_documento(self, datos_normalizados: DatosNormalizadosUniversales) -> DocumentoRecuperado:
        ...
