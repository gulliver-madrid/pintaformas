from typing import Final, Optional


from ....dependencias import Anotador
from ... import cfg
from ...elementos.herramienta import HERRAMIENTAS, Herramienta
from ...tipos import Color, CodigoAreaPF
from ...excepciones import ExcepcionPintaFormas
from ..surfaces import PygameSurfaceWrapper, SurfaceException
from .textos import TEXTOS
from .area import AreaAutoactualizable


class FUENTE: # TODO: cambiar para que no sea una clase
    tamano = 16
    tipo = "Arial"


ESTADOS_ACEPTADOS = HERRAMIENTAS
GRIS_CLARO = Color((200, 200, 200))
FONDO = GRIS_CLARO


class AreaInformativa(AreaAutoactualizable):
    codigo = CodigoAreaPF.area_informativa
    __slots__ = ('herramienta', 'anotador', 'tamano_fuente')
    anotador: Final[Anotador]
    herramienta: Optional[Herramienta]
    tamano_fuente: int

    def __init__(self) -> None:
        self.surface = None
        self.herramienta = None
        self.anotador = Anotador()
        self.tamano_fuente = FUENTE.tamano
        self.fondo = FONDO


    def registrar_cambio_herramienta(self, herramienta: Herramienta) -> None:
        self.herramienta = herramienta


    def actualizar_vista(self) -> None:
        self._rellenar_fondo()

        if self.herramienta in ESTADOS_ACEPTADOS:
            texto = TEXTOS[self.herramienta]
            tamano_fuente_original: int = FUENTE.tamano
            if len(texto) > 220:
                self.tamano_fuente = tamano_fuente_original - 2
            else:
                self.tamano_fuente = tamano_fuente_original
            self.anotar(texto)
        else:
            raise ExcepcionPintaFormas(f'Estado no conocido: {self.herramienta}')

    def anotar(self, texto: str) -> None:
        assert self.surface
        if isinstance(self.surface, PygameSurfaceWrapper):
            self.anotador.anotar(
                    texto,
                    lienzo=self.surface._surface,
                    tamano_fuente=self.tamano_fuente,
                    ajuste=80,
                    posicion=(0, 0),
                    tipo_fuente=FUENTE.tipo,
                    interlineado=2,
                    color=cfg.COLOR_NEGRO,
                    fondo=FONDO
                )
        else:
            raise SurfaceException()
