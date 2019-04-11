import string
from typing import Optional, TypeVar, Union, Protocol

from ....log_pintaformas import log
from ....dependencias import PygameEvent, nombres_pygame
from ..nombres import DIRECCIONES_ENG_TO_SP, obtener_nombre_tecla
from ..evento import Evento
from .especifico import GestorDeEventosEspecifico

CARACTERES_POSIBLES = string.ascii_lowercase + string.digits + ".,-+"

TupleStr = tuple[str, ...]


class CallbackTeclas(Protocol):
    def __call__(self) -> None:
        ...


class AccionFlecha(Protocol):
    def __call__(self, direccion: str) -> None:
        ...


KeyEquivalencias = Union[str, TupleStr]

R = TypeVar('R')


class GestorEventosTecladoBase(GestorDeEventosEspecifico[R]):
    '''Clase abstracta para los gestores de eventos de teclado'''
    equivalencias: dict[KeyEquivalencias, CallbackTeclas]
    accion_flecha: AccionFlecha
    evento: Optional[Evento]

    def procesar_evento(self, evento: Evento) -> None:
        try:
            self._procesar_evento(evento)
        except:
            self.evento = None
            raise

    def _procesar_evento(self, evento: Evento) -> None:
        self.evento = evento

        if self.flecha_pulsada:
            if hasattr(self, 'accion_flecha'):
                self.accion_flecha(self.direccion)

        else:
            tecla = self.tecla_pulsada
            log.anotar(f"La tecla pulsada es {tecla}")

            if self.algun_modo_activado():
                modos_activados = self._modos.activados

                for posible_entrada_teclado, accion in self.equivalencias.items():

                    if isinstance(posible_entrada_teclado, tuple):
                        combinacion_teclas = posible_entrada_teclado

                        if self.combinacion_equivale(tecla, modos_activados, combinacion_teclas):
                            accion()
            else:
                if tecla in self.equivalencias.keys():
                    posible_accion = self.equivalencias.get(self.tecla_pulsada)
                    if posible_accion:
                        accion = posible_accion
                        accion()

    def combinacion_equivale(self, tecla: str, modos_activados: set[str], combinacion_teclas: TupleStr) -> bool:
        # print(tecla, modos_activados)
        combinacion_realizada = (tecla, set(modos_activados))
        posible_combinacion = (combinacion_teclas[0], set(combinacion_teclas[1:]))
        return combinacion_realizada == posible_combinacion

    def algun_modo_activado(self) -> bool:
        return self._modos.alguno_activado

    def es_pulsacion_tecla(self, evento: Evento) -> bool:
        return evento.type == nombres_pygame.KEYDOWN

    @property
    def tecla_pulsada(self) -> str:
        if not self.evento:
            return ''
        assert self.evento.type == nombres_pygame.KEYDOWN
        unicode_str = self.evento.unicode
        assert isinstance(unicode_str, str)
        if unicode_str and unicode_str in CARACTERES_POSIBLES:
            return unicode_str
        else:
            return obtener_nombre_tecla(self.evento)


    @property
    def flecha_pulsada(self) -> bool:
        return self.tecla_pulsada in DIRECCIONES_ENG_TO_SP

    @property
    def direccion(self) -> str:
        return DIRECCIONES_ENG_TO_SP[self.tecla_pulsada]
