from typing import Optional

from ..auxiliares.helpers import RaizDocumentoSinNumero
from ...excepciones import NoTieneNumero

def obtener_tupla_nombre_para_la_grabacion(nombre_usado_en_la_carga: str) -> tuple[RaizDocumentoSinNumero, int]:
    try:
        raiz, numero_str = _separar_raiz_y_numero(nombre_usado_en_la_carga)
    except NoTieneNumero:
        raiz = nombre_usado_en_la_carga
        raiz, numero = _crear_tupla_nombre_para_grabar(raiz)
    else:
        numero = int(numero_str)
        raiz, numero = _crear_tupla_nombre_para_grabar(raiz, numero + 1)
    return (raiz, numero)


def _separar_raiz_y_numero(nombre: str) -> tuple[str, str]:
    quitar = 0
    for i in range(1, len(nombre)):
        if nombre[-i].isdigit():
            quitar += 1
        else:
            if quitar:
                raiz = nombre[:-quitar]
                numero_str = nombre[-quitar:]
                break
            else:
                raise NoTieneNumero
    return raiz, numero_str


def _crear_tupla_nombre_para_grabar(raiz: str, numero: Optional[int]=None) -> tuple[RaizDocumentoSinNumero, int]:
    '''
    numero, si se introduce, sera un entero
    '''
    assert not raiz[-1].isdigit(), raiz
    if raiz[-1] != '_':
        raiz += '_'
    if not numero:
        numero = 1
    return (RaizDocumentoSinNumero(raiz), numero)
