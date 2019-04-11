from typing import Sequence, Optional

from ....dependencias import PygameRect
from ...tipos import CodigoAreaPF, Posicion, Dimensiones, Color, convertir_a_tupla_tres_int, convertir_a_tupla_dos_int, Tuple3Int
from ..surfaces import GenericSurface
from .adaptadores import CreadorMuestrasPintaFormas
from .area import AreaAutoactualizable
from .escalado import Escalado

DIMS = X, Y = 0, 1

DIMENSIONES_BASE = Dimensiones((250, 150))
GRIS_MUY_OSCURO = Color((50, 50, 50))
COLOR_FONDO = GRIS_MUY_OSCURO

LADO_MUESTRA_PEQUENA_BASE = 40
ESPACIO_BASE = 12
POSICION_INICIO_BASE = Posicion((20, 18))

DISPOSICION_RECTS_MUESTRAS = (4, 2)


class AreaMuestrasColores(AreaAutoactualizable):
    '''Aun no esta desarrollada. He usado como plantilla la AreaInformativa TODO: comprobar'''
    codigo = CodigoAreaPF.area_muestras_colores
    __slots__ = ('rects_colores', 'colores_muestras', 'creador_muestras')
    rects_colores: Optional[Sequence[PygameRect]]
    colores_muestras: Sequence[Color]
    creador_muestras: CreadorMuestrasPintaFormas

    def __init__(self, creador_muestras: CreadorMuestrasPintaFormas, colores_muestras: Sequence[Tuple3Int]):
        self.surface = None
        self.rects_colores = None
        self.colores_muestras = [Color(dato_color) for dato_color in colores_muestras]
        self.creador_muestras = creador_muestras
        self.fondo = COLOR_FONDO


    def actualizar_vista(self) -> None:
        '''
        Todas las posiciones se definen de manera relativa al area_muestras_colores.
        posicion_inicio es el margen superior izq de los widgets
        muestras son las muestras de colores a elegir
        '''
        self._rellenar_fondo()
        assert self.surface

        unidad_longitud = min(self.dimensiones.dividir_por_dimensiones(DIMENSIONES_BASE))

        escalado = Escalado(unidad_longitud)

        lado_muestra_pequena = escalado(LADO_MUESTRA_PEQUENA_BASE)
        espacio = escalado(ESPACIO_BASE)

        posicion_inicio: Posicion = escalado(POSICION_INICIO_BASE)
        surface_muestras, rects_colores = self.crear_surface_y_rects_muestras(espacio, lado_muestra_pequena)
        posicion_muestras = self._obtener_posicion_muestras(posicion_inicio)

        for rect in rects_colores:
            rect.move_ip(posicion_muestras)
            rect.move_ip(self.posicion)

        self.rects_colores = rects_colores
        self.surface.blit(surface_muestras, posicion_muestras)



    def crear_surface_y_rects_muestras(self,
            espacio: int,
            lado_muestra_pequena: int
            ) -> tuple[GenericSurface, list[PygameRect]]:
        disposicion = DISPOSICION_RECTS_MUESTRAS
        ajustes_muestras = dict(
            espacio=espacio,
            lado_muestra=lado_muestra_pequena,
        )
        dimensiones_muestras = convertir_a_tupla_dos_int(
            (disposicion[dim] + 1) * espacio + disposicion[dim] * lado_muestra_pequena for dim in DIMS
        )
        datos_colores_muestras = [convertir_a_tupla_tres_int(color) for color in self.colores_muestras]
        surface_muestras, rects_colores = self.creador_muestras.crear_surface_muestras(
            datos_colores_muestras, dimensiones_muestras, disposicion, ajustes_muestras
        )
        return surface_muestras, rects_colores


    def _obtener_posicion_muestras(self, posicion_inicio: Posicion) -> Posicion:
        '''Obtiene la posicion inicial de las muestras a partir de la posicion inicial
        de los widgets y las dimensiones de la muestra_unica'''
        izquierda_muestras = 0
        posicion_muestras = Posicion((izquierda_muestras, posicion_inicio[Y]))
        return posicion_muestras
