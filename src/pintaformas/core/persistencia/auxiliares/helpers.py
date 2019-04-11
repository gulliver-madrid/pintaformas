from pathlib import Path
from typing import NewType



class RaizDocumentoSinNumero(str):
    def __init__(self, raiz: str):
        if not raiz.endswith('_'):
            raise ValueError('RaizDocumentoSinNumero debe acabar con un guion bajo')

TripleteRuta = NewType('TripleteRuta', tuple[Path, RaizDocumentoSinNumero, int])

def crear_cadena_4_caracteres(numero: int) -> str:
    return '%04d' % numero
