
from pathlib import Path

from ..ajustes_generales import AjustesGenerales
from .datos_rutas import DatosRutas, TipoOperacionPersistencia, NOMBRES

from .sistema_persistencia import SistemaPersistencia
from .auxiliares.sistema_archivos import InterfazSistemaArchivos
from .auxiliares.analizador_num_doc import AnalizadorNumerosArchivo
from .grabador import GrabadorDocumentos
from .cargador import CargadorDocumentos
from .implementacion_json import CargadorJSON, GrabadorJSON


def crear_sistema_de_persistencia(ajustes: AjustesGenerales, ruta_directorio_base_documentos: Path) -> SistemaPersistencia:
    datos_carga = crear_datos_rutas(ruta_directorio_base_documentos, TipoOperacionPersistencia.CARGA)
    datos_grabacion = crear_datos_rutas(ruta_directorio_base_documentos, TipoOperacionPersistencia.GRABACION)
    sistema_archivos = InterfazSistemaArchivos()

    cargador_especifico = CargadorJSON(sistema_archivos)
    grabador_especifico = GrabadorJSON(sistema_archivos)
    analizador_num_doc = AnalizadorNumerosArchivo()
    cargador = CargadorDocumentos(sistema_archivos, cargador_especifico, analizador_num_doc, datos_carga)
    grabador = GrabadorDocumentos(sistema_archivos, grabador_especifico, analizador_num_doc, datos_grabacion)
    return SistemaPersistencia(ajustes, cargador, grabador)



def crear_datos_rutas(ruta_directorio_documentos: Path, tipo: TipoOperacionPersistencia) -> DatosRutas:
    return DatosRutas(
        tipo,
        NOMBRES[tipo]['RAIZ_DOCUMENTO_SIN_NUMERO'],
        ruta_directorio_documentos
    )
