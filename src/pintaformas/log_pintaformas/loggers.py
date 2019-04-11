from .dependencias_log import Categorias, Logger
from .categorias import CATEGORIAS_EVENTOS, CATEGORIAS_IMPRESCINDIBLES, CATEGORIAS_PERSISTENCIA, cat


CATEGORIAS_LOGGER_GENERAL: Categorias = [
    cat.preparacion_general,
    cat.movimiento_cursor,
    cat.eventos.procesar_evento,
    cat.eventos.evento_en_gev_normal,
    cat.eventos.evento_en_gev_seleccion_circulo,
    cat.info_ciclo
]

CATEGORIAS_LOGGER_RESUMIDO: Categorias = [
    cat.preparacion_general,
]

CATEGORIAS_LOGGER_CONTROL_CAMBIOS: Categorias = [
    cat.control_cambios,
]

CATEGORIAS_SCREEN: Categorias = [
    cat.info_ciclo,
    cat.renderizador
]

LOGGER_SCREEN = Logger(
        nombre='logger_screen',
        visibles=CATEGORIAS_SCREEN +
        CATEGORIAS_IMPRESCINDIBLES
    )

LOGGERS_FICHEROS = [
    Logger(
        nombre='logger_general',
        visibles=CATEGORIAS_LOGGER_GENERAL +
        CATEGORIAS_PERSISTENCIA +
        CATEGORIAS_IMPRESCINDIBLES
    ),
    Logger(
        nombre='logger_resumido',
        visibles=CATEGORIAS_LOGGER_RESUMIDO +
        CATEGORIAS_IMPRESCINDIBLES
    ),
    Logger(
        nombre='logger_control_de_cambios',
        visibles=CATEGORIAS_LOGGER_CONTROL_CAMBIOS +
        CATEGORIAS_IMPRESCINDIBLES
    ),
    Logger(
        nombre='logger_eventos',
        visibles=CATEGORIAS_IMPRESCINDIBLES,
        imprimir_todo=CATEGORIAS_EVENTOS
    ),

    Logger(
        nombre='logger_todos_los_eventos',
        imprimir_todo=[cat.eventos.todos_los_eventos]
    ),
    Logger(
        nombre='logger_renderizador',
        visibles=CATEGORIAS_IMPRESCINDIBLES,
        imprimir_todo=[cat.renderizador, cat.cambio_herramienta]
    ),

]

# LOGGERS = [LOGGER_SCREEN] + LOGGERS_FICHEROS
LOGGERS =  LOGGERS_FICHEROS
nombres_unicos = set(logger.nombre for logger in LOGGERS)
assert len(LOGGERS) == len(nombres_unicos)
