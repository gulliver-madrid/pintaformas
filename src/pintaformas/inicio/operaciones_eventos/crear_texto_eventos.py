from typing import Mapping

from ...dependencias import pygame
from .tipos import ListaTotalDeEventos

TITULO = 'LISTA DE EVENTOS PYGAME'
TEXTO_CICLO = 'Ciclo: '
AJUSTE_NUM_CICLO = 4


def crear_texto_eventos(lista_total_eventos: ListaTotalDeEventos) -> str:
    lineas = [TITULO, '-' * len(TITULO), '']
    anterior_tipo = ''
    num_caracteres_intro = len(TEXTO_CICLO) + AJUSTE_NUM_CICLO
    linea_puntos_intro = '.' * num_caracteres_intro
    for i, lista_eventos in enumerate(lista_total_eventos):
        num_ciclo = i + 1
        intro = (TEXTO_CICLO + f'{num_ciclo}'.rjust(AJUSTE_NUM_CICLO))
        for evento in lista_eventos:
            tipo = pygame.event.event_name(evento.type)
            if anterior_tipo and tipo != anterior_tipo:
                lineas.append(intro)
                intro = linea_puntos_intro

            dicc_formateado = formatear_dicc_evento(evento.__dict__)
            sep = ': ' if dicc_formateado else ''
            descripcion_evento = f'{tipo}{sep}{dicc_formateado}'

            lineas.append(intro.ljust(14) + descripcion_evento)
            intro = linea_puntos_intro
            anterior_tipo = tipo
    return '\n'.join(lineas)



def formatear_dicc_evento(diccionario: Mapping[str, object]) -> str:
    '''Devuelve una cadena que formatea de manera sencilla un diccionario'''
    pares = []
    for clave, valor in diccionario.items():
        par = f'{clave}: {valor}'
        pares.append(par)
    texto = ', '.join(pares)
    return texto
