
from typing import Final, Optional, Protocol
from pathlib import Path

from ....log_pintaformas import log

from .gestor_documentos_sin_nombre import GestorDocumentosSinNombreParaCargador

# TYPE_CHECKING
from ..auxiliares.sistema_archivos import InterfazSistemaArchivos
from ..auxiliares.analizador_num_doc import AnalizadorNumerosArchivo
from ..implementacion_json import CargadorJSON
from ..transformar_datos.tipos import DatosNormalizadosUniversales
from ..datos_rutas import DatosRutas

class CargadorProtocol(Protocol):
    def cargar_documento(self, tupla_ruta: tuple[Path, str]) -> DatosNormalizadosUniversales:
        ...
    def listar_nombres_documentos(self, directorio: Path) -> list[str]:
        ...

class CargadorDocumentos:
    '''
    Provee el metodo cargar_documento.
    '''
    __slots__ = ('sistema_archivos', 'analizador_num_doc', 'cargador_especifico', 'datos_carga', 'gestor_documentos_sin_nombre', )
    sistema_archivos: Final[InterfazSistemaArchivos]
    cargador_especifico: Final[CargadorProtocol]
    analizador_num_doc: Final[AnalizadorNumerosArchivo]
    datos_carga: Final[DatosRutas]
    gestor_documentos_sin_nombre: Final[GestorDocumentosSinNombreParaCargador]

    def __init__(self,
            sistema_archivos: InterfazSistemaArchivos,
            cargador_especifico: CargadorProtocol,
            analizador_num_doc: AnalizadorNumerosArchivo,
            datos_carga: DatosRutas) -> None:
        self.sistema_archivos = sistema_archivos
        self.cargador_especifico = cargador_especifico
        self.analizador_num_doc = analizador_num_doc
        self.datos_carga = datos_carga
        self.gestor_documentos_sin_nombre = GestorDocumentosSinNombreParaCargador(analizador_num_doc)


    def cargar_documento(self, nombre_proporcionado: Optional[str] = None) -> tuple[DatosNormalizadosUniversales, str]:
        '''
        Carga un documento, y lo devuelve junto a su nombre.
        Si no se proporciona un nombre, se cargara el documento
        sin nombre de mayor numero.
        '''

        nombre = nombre_proporcionado or self.obtener_nombre_por_defecto()
        tupla_ruta_documento = self._obtener_tupla_ruta_documento(nombre)
        print(f'Cargando documento {nombre}')
        documento = self.cargador_especifico.cargar_documento(tupla_ruta_documento)
        log.anotar(f'El documento estaba serializado con el tipo {type(documento).__name__}')
        return documento, nombre


    def obtener_nombre_por_defecto(self) -> str:
        '''Devuelve el nombre del documento sin nombre mas reciente'''
        directorio = self.datos_carga.directorio_documentos
        print(directorio)
        nombres_documentos = self.cargador_especifico.listar_nombres_documentos(directorio)
        raiz = self.datos_carga.raiz_documento_sin_numero
        nombre = self.gestor_documentos_sin_nombre.obtener_nombre_documento_a_cargar(raiz, nombres_documentos)
        return nombre


    def _obtener_tupla_ruta_documento(self, nombre: str) -> tuple[Path, str]:
        '''Recibe el nombre del documento y devuelve su ruta'''
        return (self.datos_carga.directorio_documentos, nombre)
