from typing import Optional
from dataclasses import dataclass, field

from ...rutas import rutas
from ..core.ajustes_generales import AjustesGenerales
from ..core.persistencia.crear_sistema_de_persistencia import crear_sistema_de_persistencia
from .operaciones_eventos import ObtenedorEventos, ObtenedorEventosJSON, ObtenedorEventosPygame

# TYPE_CHECKING
from ..core.persistencia.sistema_persistencia import SistemaPersistencia

FPS_CON_EVENTOS_CARGADOS = 300

@dataclass(init=False)
class MetaComponentes:
    '''Son componentes que se aportan al programa externamente: el sistema de persistencia
    (si lo hubiere) y el obtenedor de eventos'''
    obtenedor_eventos: ObtenedorEventos
    sistema_de_persistencia: Optional[SistemaPersistencia]


@dataclass
class GestorMetaComponentes:
    '''Establece e inicializa los metacomponentes'''
    metacomponentes: MetaComponentes = field(default_factory=MetaComponentes)

    def setup(self, ajustes: AjustesGenerales) -> None:
        '''Establece el tiempo inicial, el log y los ajustes'''
        self._establecer_obtenedor_de_eventos(ajustes)
        self._setup_persistencia(ajustes)


    def obtener_metacomponentes(self) -> MetaComponentes:
        return self.metacomponentes


    def _establecer_obtenedor_de_eventos(self, ajustes: AjustesGenerales) -> None:
        eventos_a_cargar = ajustes['eventos_a_cargar']
        if eventos_a_cargar:
            assert isinstance(eventos_a_cargar, str)
            eventos_json = '.'.join((eventos_a_cargar, 'json'))
            self.metacomponentes.obtenedor_eventos = ObtenedorEventosJSON(eventos_json)
            ajustes['fps'] = FPS_CON_EVENTOS_CARGADOS
        else:
            self.metacomponentes.obtenedor_eventos = ObtenedorEventosPygame()


    def _setup_persistencia(self, ajustes: AjustesGenerales) -> None:
        '''Activa la persistencia si es necesario'''
        usar_persistencia = ajustes['usar_persistencia']
        if usar_persistencia:
            self.metacomponentes.sistema_de_persistencia = crear_sistema_de_persistencia(ajustes, rutas.directorio_documentos)
            print('Se usará persistencia\n')
        else:
            self.metacomponentes.sistema_de_persistencia = None
            print('No se usará persistencia\n')
