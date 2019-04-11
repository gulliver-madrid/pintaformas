import sys

from ..core.ajustes_generales import AjustesGenerales
from ..core.general.app import AppGeneral
from ..core.general.constructor_app import ConstructorAppGeneral
from ..log_pintaformas.ajuste_log import GestorLogPintaFormas
from .ajustes_predeterminados import AJUSTES_PREDETERMINADOS
from .analisis_argv import AnalizadorLineaComandos
from .inicio_generico import InicioGenerico
from .metacomponentes import GestorMetaComponentes
from .programa_con_persistencia import ProgramaConPersistencia
from .validador_ajustes import ValidadorAjustesUsuario


class Inicio(InicioGenerico[AppGeneral]):
    __slots__ = ('analizador_linea_comandos',)
    analizador_linea_comandos: AnalizadorLineaComandos

    def __init__(self) -> None:
        self.gestor_metacomponentes = GestorMetaComponentes()
        self.analizador_linea_comandos = AnalizadorLineaComandos()
        self.gestor_log = GestorLogPintaFormas()
        self.clase_programa = ProgramaConPersistencia
        self.constructor_app = ConstructorAppGeneral()
        self._check_componentes()

    def _establecer_ajustes(self) -> None:
        '''Establece los ajustes a partir de los argumentos de linea de comandos'''

        argumentos_linea_comandos = sys.argv[1:]
        ajustes_usuario = self.analizador_linea_comandos.obtener_ajustes_usuario(argumentos_linea_comandos)
        self.ajustes = AJUSTES_PREDETERMINADOS.copy()
        self._validar_ajustes_usuario(ajustes_usuario)
        self.ajustes.update(ajustes_usuario)

    def _validar_ajustes_usuario(self, ajustes_usuario: AjustesGenerales) -> None:
        ValidadorAjustesUsuario(ajustes_usuario, self.ajustes).validar()






if __name__ == '__main__':
    inicio = Inicio()
    inicio.activar()
