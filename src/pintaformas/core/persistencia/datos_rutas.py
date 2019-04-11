from enum import auto
from pathlib import Path

from ...libs.compartido import AutoName
from .auxiliares.helpers import RaizDocumentoSinNumero



class TipoOperacionPersistencia(AutoName):
    CARGA = auto()
    GRABACION = auto()


NOMBRES = {
    TipoOperacionPersistencia.CARGA: dict(
        RAIZ_DOCUMENTO_SIN_NUMERO=RaizDocumentoSinNumero('documento_'),
    ),
    TipoOperacionPersistencia.GRABACION: dict(
        RAIZ_DOCUMENTO_SIN_NUMERO=RaizDocumentoSinNumero('documento_'),
    ),
}


class DatosRutas:
    '''Recoge los datos relacionados con la ruta de carga o grabacion'''
    __slots__ = ('tipo', 'raiz_documento_sin_numero', 'directorio_documentos')
    tipo: TipoOperacionPersistencia
    raiz_documento_sin_numero: RaizDocumentoSinNumero
    directorio_documentos: Path

    def __init__(self, tipo: TipoOperacionPersistencia, raiz_documento_sin_numero: RaizDocumentoSinNumero, directorio_documentos: Path):
        self.tipo = tipo
        self.raiz_documento_sin_numero = raiz_documento_sin_numero
        self.directorio_documentos = directorio_documentos
