from typing import Sequence
from ..auxiliares.helpers import crear_cadena_4_caracteres

# TYPE_CHECKING
from ..auxiliares.analizador_num_doc import AnalizadorNumerosArchivo


class GestorDocumentosSinNombreParaCargador:
    '''Gestiona la obtencion de una ruta para cargar un documento sin nombre'''
    def __init__(self, analizador_num_doc: AnalizadorNumerosArchivo):
        self.analizador_num_doc = analizador_num_doc

    def obtener_nombre_documento_a_cargar(self, raiz: str, nombres_documentos: Sequence[str]) -> str:
        numero_documento = self._obtener_numero_de_documento_para_cargar(raiz, nombres_documentos)
        nombre = self._obtener_nombre_documento(raiz, numero_documento)
        return nombre

    def _obtener_numero_de_documento_para_cargar(self, raiz: str, nombres_documentos: Sequence[str]) -> int:
        numero_documento = self.analizador_num_doc.obtener_mayor_numero_documento(raiz, nombres_documentos)
        return numero_documento


    def _obtener_nombre_documento(self, raiz: str, numero_documento: int) -> str:
        num_documento_str = crear_cadena_4_caracteres(numero_documento)
        return f'{raiz}{num_documento_str}'
