import json
from pathlib import Path
from typing import TYPE_CHECKING

from ..auxiliares.sistema_archivos import InterfazSistemaArchivos

INDENTADO_JSON = 2


class GrabadorJSON:
    '''
    Ofrece acceso a los metodos y funciones de persistencia.
    Abstrae el sistema utilizado, en este caso json.
    '''

    def __init__(self, sistema_archivos: InterfazSistemaArchivos):
        self.sistema_archivos = sistema_archivos

    def grabar_documento(self, documento: object, directorio: Path, nombre_archivo: Path) -> None:
        '''
        ruta es una ruta absoluta, que incluye la extension .json
        '''
        assert nombre_archivo.name.endswith('.json')
        # print(f'GrabadorJSON: El documento que vamos a grabar es del tipo {type(documento).__name__}')

        cadena_json = json.dumps(documento, indent=INDENTADO_JSON)
        ruta = directorio / nombre_archivo
        with open(ruta, 'w') as archivo:
            archivo.write(cadena_json)
        print(f'GrabadorJSON: Documento guardado con el nombre {nombre_archivo}\n')


    def listar_nombres_documentos(self, directorio: Path) -> list[str]:
        return self.sistema_archivos.listar_directorio(directorio)


if TYPE_CHECKING:
    from ..grabador.grabador import GrabadorProtocol
    grabador_json: GrabadorJSON
    grabador: GrabadorProtocol = grabador_json
