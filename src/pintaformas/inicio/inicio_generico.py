
from typing import Generic, Type, TypeVar

from ..log_pintaformas.ajuste_log import GestorLogPintaFormas
from ..log_pintaformas import log, cat
from ..core.general.app_protocol import AppProtocol
from ..core.ajustes_generales import AjustesGenerales
from .validador_ajustes import ValidadorAjustesUsuario
from .programa_protocol import ConstructorAppProtocol, ProgramaProtocol
from .metacomponentes import GestorMetaComponentes

App = TypeVar('App', bound=AppProtocol, covariant=True)


class InicioGenerico(Generic[App]):
    __slots__ = ('ajustes', 'programa', 'gestor_metacomponentes', 'gestor_log', 'clase_programa', 'constructor_app')
    ajustes: AjustesGenerales
    clase_programa: Type[ProgramaProtocol[App]]
    programa: ProgramaProtocol[App]
    gestor_metacomponentes: GestorMetaComponentes
    gestor_log: GestorLogPintaFormas
    constructor_app: ConstructorAppProtocol[App]


    def _check_componentes(self) -> None:
        """Debe ser llamado al final de __init__() para comprobar que contiene los componentes correctos"""
        assert self.clase_programa
        assert self.gestor_metacomponentes
        assert self.gestor_log
        assert self.constructor_app

    def activar(self) -> None:
        self._setup()
        print(f"FPS: {self.ajustes['fps']}")
        metacomponentes = self.gestor_metacomponentes.obtener_metacomponentes()
        self.programa = self.clase_programa(self.ajustes, metacomponentes, self.constructor_app)
        with log.log_multinivel.abrir_autocierre(
                cat.programa, 'Inicio programa', end='\nFin programa'
        ):
            self.programa.ejecutar_programa()
        print('Hecho')


    def _setup(self) -> None:
        '''Establece el log, los ajustes y hace inicializar los metacomponentes'''
        self.gestor_log.ajustar_log(log)
        self._establecer_ajustes()
        self.gestor_metacomponentes.setup(self.ajustes)

    def _establecer_ajustes(self) -> None:
        raise NotImplementedError

    def _validar_ajustes_usuario(self, ajustes_usuario: AjustesGenerales) -> None:
        ValidadorAjustesUsuario(ajustes_usuario, self.ajustes).validar()
