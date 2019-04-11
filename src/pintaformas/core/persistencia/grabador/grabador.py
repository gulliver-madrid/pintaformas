
from pathlib import Path
from typing import Final, Optional, Protocol

from ....log_pintaformas import log, cat
from ...excepciones import (
    NoHayArchivosConEsaRaiz,
    NoHayArchivosConEsaRaizAcabadosEnNumero,
)
from ..auxiliares.helpers import TripleteRuta, RaizDocumentoSinNumero, crear_cadena_4_caracteres
from .ayudante_grabacion import obtener_tupla_nombre_para_la_grabacion


# TYPE_CHECKING
from ..auxiliares.analizador_num_doc import AnalizadorNumerosArchivo
from ..auxiliares.sistema_archivos import InterfazSistemaArchivos
from ..info_guardado_documento import InfoGuardadoDocumento
from ..datos_rutas import DatosRutas

EXTENSION = '.json'


class GrabadorProtocol(Protocol):
    def grabar_documento(self, documento: object, directorio: Path, ruta: Path) -> None:
        ...

    def listar_nombres_documentos(self, directorio: Path) -> list[str]:
        ...


class GrabadorDocumentos:
    __slots__ = ('sistema_archivos', 'grabador_especifico', 'analizador_num_doc', 'datos',)
    datos: Final[DatosRutas]
    sistema_archivos: Final[InterfazSistemaArchivos]
    grabador_especifico: Final[GrabadorProtocol]
    analizador_num_doc: Final[AnalizadorNumerosArchivo]

    def __init__(self,
            sistema_archivos: InterfazSistemaArchivos,
            grabador_especifico: GrabadorProtocol,
            analizador_num_doc: AnalizadorNumerosArchivo,
            datos_grabacion: DatosRutas) -> None:
        self.sistema_archivos = sistema_archivos
        self.grabador_especifico = grabador_especifico
        self.analizador_num_doc = analizador_num_doc
        self.datos = datos_grabacion


    def guardar_documento(self, info_guardado_documento: InfoGuardadoDocumento) -> None:
        documento, nombre_proporcionado = info_guardado_documento.extraer()
        tupla_ruta_documento = self._crear_tupla_ruta_documento_de_partida(nombre_proporcionado)
        self._guardar_documento_a_partir_de_tupla(documento, tupla_ruta_documento)


    def _crear_tupla_ruta_documento_de_partida(self, nombre_proporcionado: Optional[str]) -> TripleteRuta:
        '''
        Observa si el nombre proporcionado ya existe, en cuyo caso aumenta
        en 1 el máximo que exista, o si no lo tiene, en cuyo caso le pone el 1.
        '''

        numero_documento: int
        raiz: RaizDocumentoSinNumero
        if nombre_proporcionado:
            raiz, numero_documento = obtener_tupla_nombre_para_la_grabacion(nombre_proporcionado)
        else:
            try:
                mayor_numero_documento = self._obtener_mayor_numero_documento()
                numero_documento = mayor_numero_documento + 1
            except (NoHayArchivosConEsaRaiz, NoHayArchivosConEsaRaizAcabadosEnNumero):
                numero_documento = 1
            raiz = self.datos.raiz_documento_sin_numero
        directorio_documentos = self.datos.directorio_documentos
        triplete_ruta_documento = TripleteRuta((directorio_documentos, raiz, numero_documento))
        return triplete_ruta_documento


    def _guardar_documento_a_partir_de_tupla(self, documento: object, tupla_ruta_documento: TripleteRuta) -> None:
        '''
        Guarda un documento.
        Recibe como segundo argumento una tupla con el directorio de documentos, la raiz del documento excepto el numero,
        y el numero que le corresponde en formato int.
        '''

        directorio_docs, raiz, numero_inicial = tupla_ruta_documento
        nombre_archivo = self._crear_nombre_archivo(raiz, numero_inicial)
        log.abrir(
            cat.persistencia.guardar_documento_en_archivo,
            f'\nGuardando documento en: {nombre_archivo}'
        )
        self.grabador_especifico.grabar_documento(documento, directorio_docs,nombre_archivo)
        log.cerrar(cat.persistencia.guardar_documento_en_archivo, 'Hecho')


    def _crear_nombre_archivo(self, raiz: RaizDocumentoSinNumero, numero: int) -> Path:
        """Devuelve una ruta relativa desde el directorio de documentos"""
        numero_str = crear_cadena_4_caracteres(numero)
        nombre_documento = Path(raiz + numero_str + EXTENSION)
        return nombre_documento

    def _obtener_mayor_numero_documento(self) -> int:
        nombres = self.grabador_especifico.listar_nombres_documentos(self.datos.directorio_documentos)
        mayor_numero_documento = self.analizador_num_doc.obtener_mayor_numero_documento(
            self.datos.raiz_documento_sin_numero,
            nombres)
        return mayor_numero_documento
