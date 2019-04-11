from pathlib import Path
from typing import Optional, Sequence

from .....rutas import rutas
from ....dependencias import PygameSurface, pygame, Anotador, PygameRect
from ...tipos import Color, convertir_a_tupla_dos_int, CodigoAreaPF
from ...colores import TRANSPARENTE, NEGRO
from ..surfaces import GenericSurface, GenericSurfaceFactory
from .adaptadores import CreadorPanelHerramientasPintaFormas
from .area import AreaAutoactualizable
from .escalado import Escalado

GRIS_OSCURO = (100, 100, 100)
GRIS_MUY_OSCURO = Color((50, 50, 50))
DIMS = 0, 1

FONDO_PANEL_HERRAMIENTAS = GRIS_MUY_OSCURO  # original azul (0, 0, 200)
FONDO_HERRAMIENTA_SELECCIONADA = (255, 255, 0)


HERRAMIENTAS = ['SELECCION', 'LAPIZ', 'RECTA', 'CIRCULO']
ALTERNATIVAS = 'FLTC'
nombres_herramientas = [HERRAMIENTA.lower() for HERRAMIENTA in HERRAMIENTAS]


def crear_ruta_herramienta(nombre: str) -> Path:
    return rutas.ruta_medios / 'iconos_herramientas' / f'{nombre}.png'


class CargadorDeImagenes:
    surface_factory: GenericSurfaceFactory

    def __init__(self, surface_factory: GenericSurfaceFactory) -> None:
        self.surface_factory = surface_factory

    def cargar_imagen(self, ruta: Path) -> Optional[GenericSurface]:
        imagen: Optional[GenericSurface]
        try:
            imagen = self.surface_factory.from_surface(pygame.image.load(str(ruta)))
        except FileNotFoundError:
            imagen = None
        return imagen



RUTAS = {nombre: crear_ruta_herramienta(nombre) for nombre in nombres_herramientas}

COEF_REDUCCION = 150





class AreaHerramientas(AreaAutoactualizable):
    codigo = CodigoAreaPF.area_herramientas
    __slots__ = ('rects_herramientas', 'herramienta_seleccionada', 'creador_panel_herramientas', '_cargador_imagenes', 'creador_imagenes_desde_caracter')
    rects_herramientas: Sequence[PygameRect]
    herramienta_seleccionada: int
    creador_panel_herramientas: CreadorPanelHerramientasPintaFormas
    _cargador_imagenes: CargadorDeImagenes
    creador_imagenes_desde_caracter: 'CreadorImagenDesdeCaracter'


    def __init__(self, creador_panel_herramientas: CreadorPanelHerramientasPintaFormas, cargador_imagenes: CargadorDeImagenes, creador_imagenes_desde_caracter: 'CreadorImagenDesdeCaracter') -> None:
        self.surface = None
        self.herramienta_seleccionada = 0
        self.creador_panel_herramientas = creador_panel_herramientas
        self.fondo = FONDO_PANEL_HERRAMIENTAS
        self._cargador_imagenes = cargador_imagenes
        self.creador_imagenes_desde_caracter = creador_imagenes_desde_caracter


    def actualizar_vista(self) -> None:
        '''Tiene forma de cuadrado (aproximado)'''

        self._rellenar_fondo()
        assert self.surface

        disposicion = (2, 2)
        dimensiones_area = self.surface.get_size()
        # print(f'AreaHerramientas: {dimensiones_area}')
        minima_longitud = min(dimensiones_area)
        unidad_longitud: float = minima_longitud / COEF_REDUCCION

        escalado = Escalado(unidad_longitud)

        espacio = escalado(12)
        lado_herramienta = escalado(40)
        ajustes = dict(
            espacio=espacio,
            lado_herramienta=lado_herramienta,
        )

        dimensiones = convertir_a_tupla_dos_int(disposicion[dim] * (espacio + lado_herramienta) + espacio for dim in DIMS)

        imagenes = []
        for nombre_herramienta, alternativa in zip(HERRAMIENTAS, ALTERNATIVAS):
            imagen = self._cargar_icono_herramienta(RUTAS[nombre_herramienta.lower()], alt=alternativa)
            imagenes.append(imagen)


        herramientas: GenericSurface
        rects_herramientas: list[PygameRect]

        herramientas, rects_herramientas = \
            self.creador_panel_herramientas.crear_surface_herramientas(
                imagenes, dimensiones, disposicion, ajustes
            )

        posicion_herramientas = escalado((20, 18))
        for rect in rects_herramientas:
            rect.move_ip(posicion_herramientas)

        for i, rect in enumerate(rects_herramientas):
            if i == self.herramienta_seleccionada:
                self.surface.fill(Color(FONDO_HERRAMIENTA_SELECCIONADA), rect)
            else:
                self.surface.fill(Color(GRIS_OSCURO), rect)
        for rect in rects_herramientas:
            rect.move_ip(convertir_a_tupla_dos_int(self.posicion))
        self.surface.blit(herramientas, posicion_herramientas)
        self.rects_herramientas = rects_herramientas

    def set_indice_herramienta(self, i: int) -> None:
        assert i in range(len(HERRAMIENTAS))
        self.herramienta_seleccionada = i


    def _cargar_icono_herramienta(self, ruta: Path, alt: str) -> GenericSurface:
        imagen = self._cargador_imagenes.cargar_imagen(ruta)
        if imagen is None:
            print(f"Atención: no se pudo cargar la imagen correspondiente a la ruta {ruta}")
            imagen = self.creador_imagenes_desde_caracter.crear_imagen_alternativa(alt)
        return imagen


class CreadorImagenDesdeCaracter:
    def __init__(self, surface_factory: GenericSurfaceFactory) -> None:
        self.surface_factory = surface_factory

    def crear_imagen_alternativa(self, caracter: str) -> GenericSurface:
        assert len(caracter) == 1
        surface = PygameSurface((50, 50))
        surface.set_colorkey(TRANSPARENTE)
        anotador = Anotador(surface)
        anotador.anotar(caracter,
            tamano_fuente=36,
            posicion=(-5, -15),
            tipo_fuente='Arial',
            color=NEGRO, fondo=TRANSPARENTE
        )
        return self.surface_factory.from_surface(surface)
