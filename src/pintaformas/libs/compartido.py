from enum import Enum
from typing import Any, TypeVar


class AutoName(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> str:
        return name


def es_instancia(objeto: object, tipo: type) -> bool:
    '''Comprueba en tiempo de ejecucion que es instancia de la clase indicada, pero evitando aseverar el tipo estaticamente'''
    return isinstance(objeto, tipo)


T = TypeVar('T')


def es(objeto: T, tipo: type) -> T:
    '''Igual que es_instancia, pero realiza el assert y devuelve el objeto'''
    assert es_instancia(objeto, tipo)
    return objeto
