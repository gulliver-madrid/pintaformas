from typing import Optional, List
from .dependencias import pygame
from .ajustar_texto import preparar_texto_para_renderizar
from .tipos import Tuple3Int

INTERLINEADO_POR_DEFECTO = 12
ANCHO_FUENTE = 24 # ESTO ESTA HARDCODEADO, HAY QUE CAMBIARLO
# El problema es que en algunas aplicaciones queremos que el texto y su fondo
# se adapten a los caracteres que aportamos. En otras queremos que el fondo
# cubra una superficie mas amplia.

def crear_surface_texto_con_ajuste_de_linea(
        texto: str,
        color: Tuple3Int,
        fondo: Tuple3Int,
        ajuste: int,
        fuente_basica: pygame.font.Font,
        interlineado: Optional[int],
        *,
        ancho: Optional[int] = None,
        ) -> pygame.surface.Surface:
    '''
    Crea un surface de texto con ajuste de linea.
    '''
    if interlineado is None:
        interlineado = INTERLINEADO_POR_DEFECTO

    surfaces_lineas: List[pygame.surface.Surface] = []
    lineas = preparar_texto_para_renderizar(texto, ajuste)

    max_ancho_en_caracteres = max([len(linea) for linea in lineas])

    for linea in lineas:
        surface_linea = fuente_basica.render(linea, True, color, fondo)
        surfaces_lineas.append(surface_linea)

    alto_linea_texto = surfaces_lineas[0].get_height()
    alto_linea_total = alto_linea_texto + interlineado
    num_lineas = len(surfaces_lineas)
    # print('En crear_surfaces_texto:')
    # print(f'El ancho suministrado es de {ancho}')
    if ancho is None:
        ancho = max_ancho_en_caracteres * ANCHO_FUENTE
    # print(f'El ancho en caracteres es de {ancho}')
    surface_texto = crear_surface(ancho, alto_linea_total * num_lineas, color=fondo)

    for indice, surface in enumerate(surfaces_lineas):
        surface_texto.blit(surface, (0, indice * (alto_linea_total)))

    return surface_texto

def crear_surface(ancho: int, alto: int, *, color: Optional[Tuple3Int] = None) -> pygame.Surface:
    '''
    Crea un surface sin el uso de dobles parentesis y comprobando
    los valores de entrada.
    '''
    dimensiones = ancho, alto
    assert all([isinstance(valor, int) for valor in dimensiones]), \
           f'ancho: {ancho}, alto: {alto}'
    surface = pygame.Surface(dimensiones)
    if color:
        surface.fill(color)
    return surface
