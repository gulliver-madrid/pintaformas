from collections import defaultdict
from pathlib import Path

from ..compartido import es_instancia
from .tipos import Logger
from .fecha import obtener_fecha_actual


_DEBUG = False


class ImpresoraLog:
    __slots__ = ('_textos', '_directorio_logs')
    _textos: dict[str, list[str]]
    _directorio_logs: Path

    def __init__(self, ruta_logs: Path, comprobar_directorio: bool = True):
        if comprobar_directorio:
            assert solo_tiene_logs(ruta_logs)
        self._textos = defaultdict(list)
        self._directorio_logs = ruta_logs


    def registrar(self, mensaje: str, logger: Logger) -> None:
        '''Registra las lineas de log que seran imprimidas despues'''
        nombre_logger = logger.nombre
        assert es_instancia(nombre_logger, str)
        if nombre_logger == 'logger_screen':
            print(mensaje)
        else:
            self._textos[nombre_logger].append(mensaje)


    def imprimir_todo_en_archivos(self) -> None:
        for nombre_logger, lineas in self._textos.items():
            texto = '\n'.join(lineas)
            self.imprimir_en_archivo(texto, nombre_logger + '.log')


    def imprimir_en_archivo(self, contenido: str, nombre_archivo: str) -> None:
        if _DEBUG:
            print(f"Imprimiendo en archivo {nombre_archivo}")
        local_time = obtener_fecha_actual()
        contenido = local_time + '\n' + contenido
        ruta = self._directorio_logs / nombre_archivo
        with open(ruta, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido)


def solo_tiene_logs(ruta: Path) -> bool:
    """Devuelve True si todos los archivos del directorio indicado son logs"""
    assert ruta.is_dir()
    nombres = [ruta.name for ruta in ruta.iterdir()]
    return all(nombre.endswith('.log') for nombre in nombres)
