from typing import cast, ItemsView


def obtener_atributo(objeto: object, nombre_atributo: str) -> object:
    '''Garantiza que el valor del atributo obtenido no es un Any'''
    return getattr(objeto, nombre_atributo)


def iterar_sobre_items_atributos(objeto: object) -> ItemsView[str, object]:
    dicc_atributos: dict[str, object] = objeto.__dict__
    return dicc_atributos.items()
