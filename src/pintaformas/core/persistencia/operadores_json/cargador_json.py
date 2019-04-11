from importlib.machinery import all_suffixes
import json
from pathlib import Path

from ..auxiliares.sistema_archivos import InterfazSistemaArchivos
from ..transformar_datos.tipos import DatosNormalizadosUniversales



class CargadorJSON:
    '''
    Ofrece acceso a los metodos y funciones de persistencia.
    Abstrae el sistema utilizado, en este caso json.
    No conoce que es lo que estas guardando. Le basta que sea compatible
    con json, es decir que sean objetos python (basicos o reconstruibles).
    '''

    def __init__(self, sistema_archivos: InterfazSistemaArchivos):
        self.sistema_archivos = sistema_archivos


    def cargar_documento(self, tupla_ruta: tuple[Path, str]) -> DatosNormalizadosUniversales:

        '''
        ruta es una ruta absoluta
        El documento en algunos casos es una lista, pero podria haber
        otras opciones.
        '''
        directorio, nombre_sin_extension = tupla_ruta
        assert "." not in nombre_sin_extension, nombre_sin_extension  # TODO: validar bien
        ruta_json = directorio / (nombre_sin_extension + '.json')
        print(f'CargadorJSON: La ruta a usar para cargar el documento es {ruta_json}')
        with open(ruta_json, 'r') as archivo:
            cadena_json = archivo.read()
        documento_json_cargado: object = json.loads(cadena_json)
        print(f'CargadorJSON: Documento del tipo {type(documento_json_cargado)} cargado\n')
        assert isinstance(documento_json_cargado, (dict, list))
        doc_json_cargado_tipado: DatosNormalizadosUniversales = documento_json_cargado
        return doc_json_cargado_tipado


    def listar_nombres_documentos(self, directorio: Path) -> list[str]:
        return self.sistema_archivos.listar_directorio(directorio)



