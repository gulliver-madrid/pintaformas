
from typing import TYPE_CHECKING, Final, Generic, Optional, Sequence, TypeVar

from ..core import cfg
from ..core.ajustes_generales import AjustesGenerales
from ..core.excepciones import SalirApp
from ..core.general.app_protocol import AppProtocol
from ..core.general.tiempo import Milisegundos
from ..core.gestor_eventos.excepciones_eventos import EndInput
from ..dependencias import PygameEvent, nombres_pygame, pygame
from ..log_pintaformas import log
from .control_ciclos import ControlCiclos
from .finalizador import Finalizador
from .manejo_eventos import ManejoEventos
from .programa_protocol import ConstructorAppProtocol, ProgramaProtocol
from .tiempo.gestor_tiempo import GestorTiempo

if TYPE_CHECKING:
    from ..core.persistencia.sistema_persistencia import SistemaPersistencia
    from .metacomponentes import MetaComponentes


DETENERSE_SI_VA_LENTO = False
MILISEGUNDOS_DE_LAG_EXCESIVOS = Milisegundos(1000)


App = TypeVar('App', bound=AppProtocol, covariant=True)

class Programa(Generic[App]):
    __slots__ = (
        'app',
        'manejo_eventos',
        'persistencia',
        'control_ciclos',
        'ajustes',
        'finalizador',
        'gestor_tiempo',
        'constructor_app',
        '_cancelar_siguientes_eventos',
    )
    app: App
    manejo_eventos: Final[ManejoEventos]
    persistencia: Optional['SistemaPersistencia']
    control_ciclos: ControlCiclos
    ajustes: AjustesGenerales
    finalizador: Finalizador
    gestor_tiempo: GestorTiempo
    constructor_app: ConstructorAppProtocol[App]
    _cancelar_siguientes_eventos: bool

    def __init__(self,
            ajustes: AjustesGenerales,
            metacomponentes: 'MetaComponentes',
            constructor_app: ConstructorAppProtocol[App]
            ) -> None:
        self.ajustes = ajustes
        self.persistencia = metacomponentes.sistema_de_persistencia
        obtenedor_eventos = metacomponentes.obtenedor_eventos
        self.manejo_eventos = ManejoEventos(obtenedor_eventos, ajustes)
        self.control_ciclos = ControlCiclos()
        self.gestor_tiempo = GestorTiempo(self.control_ciclos, self.ajustes['fps'])

        usar_persistencia = bool(self.persistencia)
        self.finalizador = Finalizador(
            self.control_ciclos,
            usar_persistencia,
            self.gestor_tiempo,
            self.manejo_eventos.postprocesador_eventos,
        )
        self.constructor_app = constructor_app
        self._cancelar_siguientes_eventos = False


    def ejecutar_programa(self) -> None:
        self._procedimientos_iniciales()
        self._procedimientos_iniciales_extra()

        try:
            while True:
                self._ejecutar_un_ciclo()
        except SalirApp:
            pass
        finally:
            self._procedimientos_finales_extra()
            self.finalizador.procedimientos_finales()

    def _procedimientos_iniciales_extra(self) -> None:
        ...

    def _procedimientos_finales_extra(self) -> None:
        ...

    def _ejecutar_un_ciclo(self) -> None:
        '''Ejecuta un ciclo de la app'''
        info_ciclo = self._get_info_ciclo()
        with log.log_multinivel.abrir_autocierre('info_ciclo', info_ciclo):
            self.control_ciclos.num_ciclo += 1
            eventos = self.manejo_eventos.obtener_eventos()
            if self._cancelar_siguientes_eventos:
                eventos.clear()
                print("Eventos cancelados")
                self._cancelar_siguientes_eventos = False
            try:
                self.app.ejecutar_ciclo(eventos)
            except EndInput:
                self._cancelar_siguientes_eventos = True
                print("Se cancelarán los próximos eventos")
            self.gestor_tiempo.ralentizar()
            self._chequeo_lag(eventos)

    def _procedimientos_iniciales(self) -> None:
        """Inicializa pygame y la app"""
        titulo_inicial = self.ajustes['titulo']
        self._iniciar_pygame()
        self._crear_ventana(titulo_inicial)
        self.app = self.constructor_app.crear_app(titulo_inicial)
        self.app.iniciar()

        self.gestor_tiempo.establecer_medidor_tiempo(self.constructor_app.medidor_tiempo)
        self.gestor_tiempo.activar_reloj()

    def _iniciar_pygame(self) -> None:
        pygame.display.init()
        pygame.key.set_repeat(cfg.ESPERA_INICIAL_REPETICION_TECLA,
                              cfg.INTERVALO_ENTRE_REPETICION_TECLA)

    def _crear_ventana(self, titulo: str) -> None:
        dimensiones_ventana = self.ajustes['dimensiones']
        pygame.display.set_mode(dimensiones_ventana, nombres_pygame.RESIZABLE)
        pygame.display.set_caption(titulo)


    def _get_info_ciclo(self) -> str:
        tiempo_actual = self.gestor_tiempo.get_tiempo_actual()
        info_log = f'\nCiclo: {self.control_ciclos.num_ciclo}. Tiempo: {tiempo_actual}'
        return info_log

    def _chequeo_lag(self, eventos: Sequence[PygameEvent]) -> None:
        if DETENERSE_SI_VA_LENTO and self._lag_no_justificado(eventos):
            print('Más de un segundo de lag')
            breakpoint()

    def _lag_no_justificado(self, eventos: Sequence[PygameEvent]) -> bool:
        return (
            not _incluyen_video_resize(eventos) and
            self.gestor_tiempo.data.duracion_ultimo_ciclo > MILISEGUNDOS_DE_LAG_EXCESIVOS
            )



def _incluyen_video_resize(eventos: Sequence[PygameEvent]) -> bool:
    return any(evento.type == nombres_pygame.VIDEORESIZE for evento in eventos)


if TYPE_CHECKING:
    class AppValida(AppProtocol):
        ...
    app: AppValida
    instancia: Programa[AppValida]
    protocol: ProgramaProtocol[AppValida] = instancia
