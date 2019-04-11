
from typing import Sequence
from ...excepciones import NoHayArchivosConEsaRaiz, NoHayArchivosConEsaRaizAcabadosEnNumero


class AnalizadorNumerosArchivo:
    '''Analiza el directorio para obtener el mayor numero de documento sin nombre'''

    def obtener_mayor_numero_documento(self, raiz_archivo_sin_numero: str, nombres_en_directorio: Sequence[str]) -> int:
        '''
        Obtiene el numero del documento guardado de mayor numero
        (presumiblemente que fue guardado en ultimo lugar).
        Ejemplo:
            obtener_mayor_numero_documento('doc_num_', ['un_nombre.json', 'doc_num_001.json', 'doc_num_002.json', 'doc_num_007.json', 'otro_nombre.json'])
            Devuelve: 7

        '''
        nombres_documentos = [
            nombre for nombre in nombres_en_directorio
            if nombre.startswith(raiz_archivo_sin_numero)
            ]
        tamano_raiz = len(raiz_archivo_sin_numero)
        if len(nombres_documentos):
            numeros_de_documento = self._extraer_numeros_de_documento(tamano_raiz, nombres_documentos)
            if numeros_de_documento:
                maximo = max(numeros_de_documento)
            else:
                raise NoHayArchivosConEsaRaizAcabadosEnNumero(raiz_archivo_sin_numero)
        else:
            raise NoHayArchivosConEsaRaiz(raiz_archivo_sin_numero)
        assert maximo > 0
        return maximo


    @staticmethod
    def _extraer_numeros_de_documento(tamano_raiz: int, nombres: list[str]) -> list[int]:
        '''
        Recibe la lista de nombres y devuelve una lista de enteros
        ['documento_001', 'documento_002', 'documento_007', ...] => [1, 2, 7, ...]
        '''
        numeros_de_documento = []
        for nombre in nombres:
            nombre_sin_extension, extension = nombre.split('.')
            parte_que_no_es_raiz = nombre_sin_extension[tamano_raiz:]
            try:
                entero = int(parte_que_no_es_raiz)
            except ValueError:
                pass
            else:
                numeros_de_documento.append(entero)

        return numeros_de_documento
