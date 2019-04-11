
from ...dependencias import pygame
from .evento import Evento

DIRECCIONES_SP_TO_ENG = dict(
    izquierda='left',
    derecha='right',
    arriba='up',
    abajo='down'
)

DIRECCIONES_ENG_TO_SP = {eng: sp for sp, eng in DIRECCIONES_SP_TO_ENG.items()}

DIRECTIONS = list(DIRECCIONES_ENG_TO_SP)


def obtener_nombre_tecla(evento: Evento) -> str:
    tecla_pygame = evento.key
    assert isinstance(tecla_pygame, int)
    try:
        nombre = pygame.key.name(tecla_pygame)
    except UnicodeDecodeError:
        raise
    return nombre
