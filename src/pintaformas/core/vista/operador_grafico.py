from typing import Iterable, Union

from ...core.vista.surfaces import (GenericSurface, GenericSurfaceFactory,
                                    RectAmpliado)
from ...log_pintaformas import cat, log
from ..tipos import (Color, Dimensiones, Posicion, PosicionEnPantalla,
                     Tuple2Int, convertir_a_tupla_dos_int,
                     convertir_a_tupla_tres_int)
from ..vista.objeto_capas_internas import ObjetoConCapasInternas

SurfaceConPosicion = tuple[GenericSurface, PosicionEnPantalla]


MAXIMO_TAMANO_SURFACE = 2000

DIMS = 0, 1

PosicionValida = Union[PosicionEnPantalla, Tuple2Int]



class OperadorGrafico:
    __slots__ = 'surface_factory'
    surface_factory: GenericSurfaceFactory

    def __init__(self, surface_factory: GenericSurfaceFactory):
        self.surface_factory = surface_factory

    def rellenar(self, surface: GenericSurface, color: Color) -> None:
        try:
            surface.fill(color)
        except Exception as error:
            raise RuntimeError(f'No se pudo rellenar {surface} con {color}') from error


    def dibujar_circulo(self, surface: GenericSurface, color: Color, posicion: PosicionValida, radio: int, ancho: int = 0) -> None:
        tupla_posicion = convertir_a_tupla_dos_int(posicion)
        tupla_color = convertir_a_tupla_tres_int(color)
        surface.draw_circle(tupla_color, tupla_posicion, radio, ancho)


    def dibujar_rectangulo(self, surface: GenericSurface, color: Color, rect: RectAmpliado) -> None:
        tupla_color = convertir_a_tupla_tres_int(color)
        surface.draw_rect(tupla_color, rect)


    def dibujar_linea(self,
            surface: GenericSurface,
            color: Color,
            inicio: PosicionValida,
            fin: PosicionValida,
            ancho: int) -> None:
        tupla_inicio = convertir_a_tupla_dos_int(inicio)
        tupla_fin = convertir_a_tupla_dos_int(fin)
        tupla_color = convertir_a_tupla_tres_int(color)
        surface.draw_line(tupla_color, tupla_inicio, tupla_fin, ancho)
        # Se anaden circulos en los extremos para darle un estilo mas natural
        radio_extremos = (ancho - 1) // 2
        self.dibujar_circulo(surface, color, inicio, radio_extremos)
        self.dibujar_circulo(surface, color, fin, radio_extremos)


    def crear_surface(self, dimensiones: Union[Dimensiones, Tuple2Int]) -> GenericSurface:
        if any(dimensiones[dim] > MAXIMO_TAMANO_SURFACE for dim in DIMS):
            raise ValueError(dimensiones)
        return self.surface_factory.from_size(convertir_a_tupla_dos_int(dimensiones))



    def pegar_capas(self, capa_base: ObjetoConCapasInternas, surfaces_con_posicion: Iterable[SurfaceConPosicion]) -> None:
        assert capa_base.surface
        secuencia_tuplas = [
            (surface, convertir_a_tupla(posicion))
            for surface, posicion in surfaces_con_posicion
        ]
        num_surfaces = len(secuencia_tuplas)
        log.anotar(f"Pegando {num_surfaces} surfaces", cat.operador_grafico)
        capa_base.surface.blits(blit_sequence=secuencia_tuplas)


def convertir_a_tupla(posicion: Posicion) -> Tuple2Int:
    x, y = posicion
    return (x, y)
