from typing import Final, Optional

from ...dependencias import PygameRect
from .. import cfg
from ..general.control_capas import ControlDeCapas, ControlObjetosVista
from ..tipos import Dimensiones
from ..tipos.cev import LIENZO_DIBUJO_SELECCION, CodigoObjetoEspecial
from .areas.area import Area
from .capas import CapaContenedora
from .generador_referencias import (GeneradorReferenciasClaveVista,
                                    ReferenciasClave)

ANCHO_RELATIVO_AREA = dict(
    informativa=0.45,
    herramientas=0.15,
    color_seleccionado=0.15,
)
ANCHO_RELATIVO_AREA['muestras_colores'] = 1 - sum(ANCHO_RELATIVO_AREA.values())

POSICION_RELATIVA_AREA = dict(
    informativa=0,
    herramientas=ANCHO_RELATIVO_AREA['informativa'],
    color_seleccionado=sum(ANCHO_RELATIVO_AREA[nombre] for nombre in ('informativa', 'herramientas')),
    muestras_colores=sum(ANCHO_RELATIVO_AREA[nombre] for nombre in ('informativa', 'herramientas', 'color_seleccionado')),
)



class CreadorRectsAreas:
    __slots__ = ('generador_refs_clave', '_control_objetos_vista', '_referencias_clave')
    generador_refs_clave: Final[GeneradorReferenciasClaveVista]
    _control_objetos_vista: Final[ControlObjetosVista]
    _referencias_clave: Optional[ReferenciasClave]

    def __init__(self,
            generador_refs_clave: GeneradorReferenciasClaveVista,
            control_capas: ControlDeCapas):
        self.generador_refs_clave = generador_refs_clave
        self._control_objetos_vista = control_capas.control_objetos_vista
        self._referencias_clave: Optional[ReferenciasClave] = None

    @property
    def referencias_clave(self) -> ReferenciasClave:
        if not self._referencias_clave:
            self._referencias_clave = self.generador_refs_clave.obtener_referencias_clave(porcentaje_separacion_vertical=cfg.PORCENTAJE_AREA_DIBUJO)
        return self._referencias_clave

    def borrar_referencias_clave(self) -> None:
        self._referencias_clave = None


    def anadir_rects(self, dicc_areas: dict[str, Area]) -> None:
        for nombre, area in dicc_areas.items():
            rect = self.crear_rect_area(nombre)
            area.set_rect(rect)
            if nombre == 'dibujo':
                capa_dibujo = self._control_objetos_vista.get_capa(CodigoObjetoEspecial.dibujo)
                assert isinstance(capa_dibujo, CapaContenedora)
                tamano_rect_area_dibujo = area.rect.size
                dimensiones_capa_dibujo = Dimensiones(tamano_rect_area_dibujo)
                capa_dibujo.set_dimensiones(dimensiones_capa_dibujo)
            for codigo in LIENZO_DIBUJO_SELECCION:
                capa = self._control_objetos_vista.get_capa(codigo)
                capa.surface = None


    def crear_rect_area(self, nombre: str) -> PygameRect:
        if nombre == 'dibujo':
            return self.crear_rect_area_dibujo()
        elif nombre in (
            'informativa',
            'herramientas',
            'muestras_colores',
            'color_seleccionado'
            ):
            return self.crear_rect_area_zona_inferior(nombre)
        else:
            raise NameError(nombre)


    def crear_rect_area_dibujo(self) -> PygameRect:
        ancho_ventana, _, separacion_vertical = self.referencias_clave.get_values()
        dimensiones_area_dibujo = (ancho_ventana, separacion_vertical)
        rect_area_dibujo = PygameRect((0, 0) + dimensiones_area_dibujo)
        return rect_area_dibujo




    def crear_rect_area_zona_inferior(self, nombre: str) -> PygameRect:
        ancho_ventana, alto_ventana, separacion_vertical = self.referencias_clave.get_values()
        alto_area = alto_ventana - separacion_vertical
        dimensiones = (round(ancho_ventana * ANCHO_RELATIVO_AREA[nombre]), alto_area)
        posicion = (round(ancho_ventana * POSICION_RELATIVA_AREA[nombre]), separacion_vertical)
        rect_area = PygameRect(posicion + dimensiones)
        return rect_area
