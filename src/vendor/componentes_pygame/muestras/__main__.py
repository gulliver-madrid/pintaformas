import pygame
from .colores import COLORES, NOMBRES_COLORES
from .cursores import SelectorCursor
from .widget_muestras import CreadorMuestras
X, Y = 0, 1
TITULO = 'Demo Widget Muestras'
FPS = 30

DIMENSIONES_VENTANA = (800, 600)


DIMENSIONES_WIDGET = (400, 208)
TEXTO_INTERPRETE_INTEGRADO = '''
Intérprete integrado.
Introduce comando a ejecutar y pulsa ENTER (no uses esto si no entiendes las implicaciones!!
Usa una linea vacia y ENTER para salir de este interprete)
'''
DISPOSICIONES = [
    (4, 2),
    (3, 2),
    (3, 1),
    (2, 2),
]
def crear_muestras(ventana, disposicion, dimensiones=None, ajustes=None):
    creador_muestras = CreadorMuestras()
    if not dimensiones:
        dimensiones = DIMENSIONES_WIDGET
    muestras, rects_colores = creador_muestras.crear_surface_muestras(COLORES, dimensiones, disposicion, ajustes)
    UBICACION = (200, 196)
    ventana.blit(muestras, UBICACION)
    for rect in rects_colores:
        rect.move_ip(*UBICACION)
    return rects_colores

def main():

    pygame.init()

    pygame.display.set_caption(TITULO)
    ventana = pygame.display.set_mode(DIMENSIONES_VENTANA)
    reloj = pygame.time.Clock()
    selector_cursor = SelectorCursor(pygame)
    rects_colores = crear_muestras(ventana, DISPOSICIONES[0])

    indice_disp = 0
    seguir = True
    actualizar = True
    while seguir:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                seguir = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(rects_colores):
                    if rect.collidepoint(*evento.pos):
                        print(f'¡Has elegido el color {NOMBRES_COLORES[i].lower()}!')
            elif evento.type == pygame.MOUSEMOTION:
                for i, rect in enumerate(rects_colores):
                    if rect.collidepoint(*evento.pos):
                        if not selector_cursor.usando_cursor_seleccion:
                            selector_cursor.set_seleccion()
                        break
                else:
                    if selector_cursor.usando_cursor_seleccion:
                        selector_cursor.set_normal()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_i:
                    print(TEXTO_INTERPRETE_INTEGRADO)
                    while True:
                        codigo = input('\n: ')
                        if codigo:
                            try:
                                exec(codigo)
                            except Exception as error:
                                print(error)
                        else:
                            break
                elif evento.key == pygame.K_1:
                    ventana.fill((0,0,0))
                    print('Cambiar muestras')
                    indice_disp += 1
                    if indice_disp >= len(DISPOSICIONES):
                        indice_disp = 0
                    rects_colores = crear_muestras(ventana, DISPOSICIONES[indice_disp])
                    actualizar = True

                elif evento.key == pygame.K_2:
                    ventana.fill((0,0,0))
                    print('Cambiar más parámetros')
                    disposicion = (1, 1)
                    espacio = 16
                    lado_muestra = 80 + 80 +16
                    ajustes= dict(
                        espacio = espacio,
                        lado_muestra = lado_muestra,
                    )
                    dimensiones= (2*espacio + lado_muestra, 2*espacio + lado_muestra)
                    rects_colores = crear_muestras(ventana, disposicion, dimensiones, ajustes)
                    actualizar = True



        if actualizar:
            pygame.display.update()
            actualizar = False
        reloj.tick(FPS)


if __name__ == '__main__':
    main()
