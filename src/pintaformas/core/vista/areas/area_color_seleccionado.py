from ...tipos import Dimensiones, Posicion, Color, convertir_a_tupla_tres_int, convertir_a_tupla_dos_int, CodigoAreaPF
from ..surfaces import GenericSurface
from .area import AreaAutoactualizable
from .adaptadores import CreadorMuestrasPintaFormas
from .escalado import Escalado

DIMS = X, Y = 0, 1

DIMENSIONES_BASE = Dimensiones((150, 150))

GRIS_MUY_OSCURO = Color((50, 50, 50))
COLOR_FONDO = GRIS_MUY_OSCURO

LADO_MUESTRA_PEQUENA_BASE = 40
ESPACIO_BASE = 12
POSICION_INICIO_BASE = Posicion((20, 18))


class AreaColorSeleccionado(AreaAutoactualizable):
    codigo = CodigoAreaPF.area_color_seleccionado
    __slots__ = ('color_seleccionado', 'creador_muestras', )

    color_seleccionado: Color
    creador_muestras: CreadorMuestrasPintaFormas


    def __init__(self, creador_muestras: CreadorMuestrasPintaFormas) -> None:
        self.surface = None
        self.creador_muestras = creador_muestras
        self.fondo = COLOR_FONDO


    def actualizar_vista(self) -> None:  # VALORES ORIGINALES EN COMENTARIOS
        '''
        Todas las posiciones se definen de manera relativa al area_muestras_colores.
        posicion_inicio es el margen superior izq de los widgets
        muestra_unica es la muestra de color seleccionado
        muestras son las muestras de colores a elegir
        espacio_entre_widgets es el espacio entre ambas
        '''

        self._rellenar_fondo()
        assert self.surface

        unidad_longitud = min(self.dimensiones.dividir_por_dimensiones(DIMENSIONES_BASE))
        escalado = Escalado(unidad_longitud)
        lado_muestra_pequena = escalado(LADO_MUESTRA_PEQUENA_BASE)
        espacio = escalado(ESPACIO_BASE)

        posicion_inicio = escalado(POSICION_INICIO_BASE)

        surface_muestra_unica = self.crear_surface_muestra_unica(lado_muestra_pequena, espacio)
        self.surface.blit(surface_muestra_unica, posicion_inicio)


    def crear_surface_muestra_unica(self, lado_muestra_pequena: int, espacio: int) -> GenericSurface:
        lado_muestra_unica = lado_muestra_pequena * 2 + espacio  # 92
        dimensiones_muestra_unica = Dimensiones(lado_muestra_unica + espacio * 2 for dim in DIMS)  # 92 + 24 = 116

        ajustes = dict(
            espacio=espacio,
            lado_muestra=lado_muestra_unica,
        )

        color_muestra_unica = convertir_a_tupla_tres_int(self.color_seleccionado)
        assert isinstance(color_muestra_unica, tuple)
        dimensiones_muestra_unica_dos_int = convertir_a_tupla_dos_int(dimensiones_muestra_unica)

        surface_muestra_unica, _rects = self.creador_muestras.crear_surface_muestras(
            [color_muestra_unica],
            dimensiones_muestra_unica_dos_int,
            (1, 1),
            ajustes
        )
        return surface_muestra_unica
