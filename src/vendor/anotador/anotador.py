from typing import Optional, Union
from .tipos import Tuple2Int, Tuple3Int, Tuple4Int
from .dependencias import pygame, nombres_pygame
# Utilidad para uso en consola
from .texto_caperucita import txt as texto_prueba
from .cuadro_texto import CuadroDeTexto
from .crear_surfaces_texto import crear_surface_texto_con_ajuste_de_linea



DIMENSIONES_VENTANA = (1000, 600)
COLOR_FONDO_PREDETERMINADO = (80, 80, 160)
COLOR_TEXTO = (200, 200, 200)

MARGEN_IZQUIERDO_RECUADRO = 20
MARGEN_INFERIOR_RECUADRO = 10
TIPO_FUENTE_PREDETERMINADA = 'monospace'  # es monoespacio
TAMANO_FUENTE_POR_DEFECTO = 20



def crear_anotador() -> 'Anotador':
    '''
    Setup de objeto Anotador para uso en consola. Inicializa pygame y pasa
    la ventana principal como lienzo.
    '''

    if not pygame.display.get_init():
        pygame.init()
        pygame.display.set_mode(DIMENSIONES_VENTANA)
    lienzo = pygame.display.get_surface()
    return Anotador(lienzo)


class Anotador:
    def __init__(self, lienzo: Optional[pygame.surface.Surface] = None):
        self.lienzo = lienzo

    def anotar(self,
            texto: Optional[str] = None,
            *,
            lienzo: Optional[pygame.surface.Surface] = None,
            tamano_fuente: Optional[int] = None,
            interlineado: Optional[int] = None,
            tipo_fuente: Optional[str] = None,
            ajuste: Optional[int] = None,
            actualizar: bool = False,
            fondo: Optional[Tuple3Int] = None,
            posicion: Optional[Union[int, Tuple2Int]] = None,
            color: Optional[Tuple3Int] = None,
            ancho: Optional[int] = None,
            quitar_margenes_cuadro_texto: bool = False,
            limitar_ancho: bool = False) -> Optional[Tuple4Int]:
        '''
        Construye un cuadro de texto con las caracteristicas especificadas
        y lo pega en el lienzo.
        En algunos casos, devuelve un rect
        '''
        if lienzo:
            self.lienzo = lienzo
        else:
            if not self.lienzo:
                raise RuntimeError("No se establecio ningun lienzo (usar kwarg 'lienzo' con un surface)")
        if not pygame.display.get_init():
            raise Exception("Para utilizar el metodo anotar es necesario iniciar antes pygame.")
        if not fondo:
            fondo = COLOR_FONDO_PREDETERMINADO
        if not texto:
            texto = ""
        if not color:
            color = COLOR_TEXTO
        # print(f'En anotador: limitar_ancho={limitar_ancho}')
        if not ancho:
            if limitar_ancho:
                ancho = None
            else:
                ancho = self.lienzo.get_width() - 40

        surfaceTexto = self.crear_surface_texto(
            texto,
            tamano_fuente,
            color=color,
            tipo_fuente=tipo_fuente,
            fondo=fondo,
            ajuste=ajuste,
            interlineado=interlineado,
            ancho_texto=ancho
        )
        posicion_cuadro_texto: Optional[Tuple2Int]
        margen_extra_cuadro_texto: Optional[Tuple2Int]
        if quitar_margenes_cuadro_texto:
            posicion_cuadro_texto = (0, 0)
            margen_extra_cuadro_texto = (0, 0)
        else:
            posicion_cuadro_texto = None
            margen_extra_cuadro_texto = None
        cuadro_texto = CuadroDeTexto(
            surfaceTexto,
            fondo,
            ancho_minimo=ancho,
            posicion=posicion_cuadro_texto,
            margen_extra=margen_extra_cuadro_texto
        )

        retorno: Optional[Tuple4Int]
        if posicion != None:
            if isinstance(posicion, int):
                if posicion < 0:
                    posicion_y_desde_abajo = (0 - posicion)
                    # posicion_cartesiana = (MARGEN_IZQUIERDO_RECUADRO)
                    posicion_y_desde_abajo = abs(posicion)
                    posicion_cartesiana = (MARGEN_IZQUIERDO_RECUADRO, posicion_y_desde_abajo)
                    self.pegar_desde_abajo(cuadro_texto, posicion_cartesiana)
                    retorno = None
                else:
                    posicion_y = posicion
                    posicion_x = MARGEN_IZQUIERDO_RECUADRO
                    posicion_xy = (posicion_x, posicion_y)
            elif isinstance(posicion, tuple):
                posicion_xy = posicion
            else:
                raise TypeError("El argumento 'posicion' debe ser un entero o una tupla")
            self.lienzo.blit(cuadro_texto, posicion_xy)
            retorno = posicion_xy + cuadro_texto.get_size()
        else:
            posicion_cartesiana = (MARGEN_IZQUIERDO_RECUADRO, MARGEN_INFERIOR_RECUADRO)
            self.pegar_desde_abajo(cuadro_texto, posicion_cartesiana)
            retorno = None
        if actualizar:
            pygame.display.update()
        return retorno

    def crear_surface_texto(self,
            texto: str,
            tamano_fuente: Optional[int] = None,
            *,
            fondo: Optional[Tuple3Int] = None,
            color: Tuple3Int,
            ajuste: Optional[int] = None,
            ancho_texto: Optional[int] = None,
            tipo_fuente: Optional[str] = None,
            interlineado: Optional[int] = None
            ) -> pygame.surface.Surface:
        '''Metodo publico. Crea un surface de texto.'''
        assert self.lienzo
        if not tamano_fuente:
            tamano_fuente = TAMANO_FUENTE_POR_DEFECTO
        if not fondo:
            fondo = COLOR_FONDO_PREDETERMINADO
        # if not ancho_texto:
        #     ancho_texto = self.lienzo.get_width()
        if not tipo_fuente:
            tipo_fuente = TIPO_FUENTE_PREDETERMINADA
        modulo_font_iniciado = pygame.font.get_init()
        if not modulo_font_iniciado:
            pygame.font.init()
        fuente_basica = pygame.font.SysFont(tipo_fuente, tamano_fuente)
        # print(f'En crear_surface_texto: ancho_texto={ancho_texto}')
        if ajuste:
            surfaceTexto = crear_surface_texto_con_ajuste_de_linea(texto, color,
                fondo, ajuste, fuente_basica, interlineado, ancho=ancho_texto)
        else:
            surfaceTexto = fuente_basica.render(texto, True, color, fondo)
        return surfaceTexto


    def pegar_desde_abajo(self,
            cuadro_texto: pygame.surface.Surface,
            posicion_cartesiana: Tuple2Int) -> None:
        '''
        posicion_cartesiana son las coordenadas x, y desde abajo
        (como si fuera el eje ++ de las coordenadas cartesianas)
        '''
        assert self.lienzo
        x, y_desde_abajo = posicion_cartesiana
        alto_recuadro = cuadro_texto.get_height()

        alto_ventana = self.lienzo.get_height()
        y_desde_arriba = alto_ventana - (y_desde_abajo + alto_recuadro)
        self.lienzo.blit(cuadro_texto, (x, y_desde_arriba))



def demo() -> None:

    pygame.init()
    pygame.display.set_mode(DIMENSIONES_VENTANA)
    pygame.display.set_caption("Demo Anotador")
    lienzo = pygame.display.get_surface()
    a = Anotador(lienzo)
    a.anotar(texto_prueba, actualizar=True, fondo=(255, 117, 20), ajuste=40)
    reloj = pygame.time.Clock()
    seguir = True
    while seguir:
        for evento in pygame.event.get():
            if (evento.type == pygame.QUIT or
                evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                seguir = False
        reloj.tick(10)
    pygame.quit()


if __name__ == '__main__':
    demo()
