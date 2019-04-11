from typing import Optional, Sequence

from ...log_pintaformas import log

from ..ajustes_generales import AjustesGenerales
from ..elementos.forma import Forma
from ..general.doc_en_memoria import DocumentoEnMemoria
from .transformar_datos.transformar_datos import TransformarDatos
from .info_guardado_documento import InfoGuardadoDocumento

# TYPE_CHECKING
from .cargador import CargadorDocumentos
from .grabador import GrabadorDocumentos
from .transformar_datos.tipos import DatosNormalizadosUniversales
from .transformar_datos.formatos_documento import Documento

DocumentoBase = tuple[DocumentoEnMemoria, Sequence[Forma]]

class SistemaPersistencia:
    '''
    Ofrece persistencia, cargando un documento guardado si es necesario,
    y grabando el resultado al final.
    Se ocupa de la normalizacion de datos.
    Abstrae la implementación concreta de la gestion de persistencia
    a partir de metodos en los que se puede aportar, o no, un nombre
    para la grabacion o la carga de documentos
    '''

    def __init__(self, ajustes: AjustesGenerales, cargador: CargadorDocumentos, grabador: GrabadorDocumentos) -> None:
        self.ajustes = ajustes
        self.cargador = cargador
        self.grabador = grabador


    def cargar_dibujo_guardado_en_espacio_de_trabajo(self) -> tuple[Documento, str]:
        log.anotar('\nSistemaPersistencia.cargar_dibujo_guardado_en_espacio_de_trabajo()')
        nombre_proporcionado = self.ajustes['nombre_documento_proporcionado_por_el_usuario']
        documento_en_proceso, nombre = self._cargar_documento(nombre_proporcionado)

        if documento_en_proceso != None:
            if isinstance(documento_en_proceso, list):
                if not all(isinstance(elemento, dict) for elemento in documento_en_proceso):
                    raise ValueError('El documento no esta normalizado')
            else:
                log.anotar('En este caso, el documento en proceso es un diccionario')
            transformar_datos = TransformarDatos()
            assert isinstance(documento_en_proceso, (dict, list)) # necesario para mypy
            documento = transformar_datos.convertir_datos_a_objetos(documento_en_proceso)
            log.anotar(f'Numero de capas importadas: {len(documento.capas)}')
        else:
            raise ValueError('El documento no existe')
        log.anotar(f'nSistemaPersistencia: el documento que estamos cargando es del tipo {type(documento).__name__}')
        return documento, nombre



    def guardar_dibujo(self, documento_base: DocumentoBase) -> None:
        log.anotar('\nSistemaPersistencia.guardar_dibujo()')
        nombre_proporcionado = self.ajustes['nombre_documento_proporcionado_por_el_usuario']

        transformar_datos = TransformarDatos()
        documento_normalizado = transformar_datos.normalizar_datos(documento_base)

        if nombre_proporcionado:
            assert isinstance(nombre_proporcionado, str)
            info_guardado_documento = InfoGuardadoDocumento(documento_normalizado, nombre_proporcionado)
        else:
            info_guardado_documento = InfoGuardadoDocumento(documento_normalizado)
        self._guardar_documento(info_guardado_documento)


    def _cargar_documento(self, nombre_proporcionado: Optional[str] = None) -> tuple[DatosNormalizadosUniversales, str]:
        documento_json_cargado, nombre = self.cargador.cargar_documento(nombre_proporcionado)
        return documento_json_cargado, nombre

    def _guardar_documento(self, info_guardado_documento: InfoGuardadoDocumento) -> None:
        self.grabador.guardar_documento(info_guardado_documento)
