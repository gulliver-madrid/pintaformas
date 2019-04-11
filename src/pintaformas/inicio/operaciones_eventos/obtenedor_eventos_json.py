import json
from pathlib import Path
from typing import TYPE_CHECKING, cast


from ...dependencias import pygame, nombres_pygame
from ...inicio.operaciones_eventos.rutas import RUTA_EVENTOS_RELATIVA
from ...core.tipos import convertir_a_tupla_dos_int, \
    convertir_a_tupla_tres_int
from .tipos import ValorOrigenJSON, AtributoPygameEvent, DiccEvento, \
    EventosJSONTotales, EventosDeUnCiclo, \
    ListaTotalDeEventos



def get_ruta_carga_eventos(eventos_json: str) -> Path:
    ruta_absoluta = Path(__file__)
    assert ruta_absoluta.is_absolute()
    ruta_este_directorio = ruta_absoluta.parent
    directorio_carga = ruta_este_directorio / RUTA_EVENTOS_RELATIVA
    assert directorio_carga.exists(), directorio_carga
    return directorio_carga / eventos_json


class ObtenedorEventosJSON:
    eventos_totales: ListaTotalDeEventos

    def __init__(self, eventos_json: str, *, fast: bool = True, carga_automatica: bool = True):
        self.indice_obtencion = 0
        self.ruta_carga = get_ruta_carga_eventos(eventos_json)
        if carga_automatica:
            self.eventos_totales = self.cargar_eventos()
        self.fast = fast

    def obtener_eventos(self) -> EventosDeUnCiclo:
        eventos_prioritarios = self.detectar_eventos_prioritarios()
        if eventos_prioritarios:
            return eventos_prioritarios
        while True:
            self.indice_obtencion += 1
            eventos = self.eventos_totales[self.indice_obtencion]
            if self.fast and not eventos:
                continue
            else:
                break
        return eventos

    def detectar_eventos_prioritarios(self) -> EventosDeUnCiclo:
        eventos_prioritarios = []
        eventos_en_tiempo_real = pygame.event.get()
        for evento in eventos_en_tiempo_real:
            if (
                evento.type == nombres_pygame.QUIT or
                (
                    evento.type == nombres_pygame.KEYDOWN and evento.key == nombres_pygame.K_ESCAPE
                )
            ):
                eventos_prioritarios.append(evento)
        return eventos_prioritarios

    def cargar_eventos(self) -> ListaTotalDeEventos:
        '''Carga los eventos desde el archivo json hasta tener todos los eventos pygame
        estruturados'''
        assert self.ruta_carga.exists(), self.ruta_carga
        with open(self.ruta_carga, 'r') as archivo:
            cadena_json = archivo.read()
        eventos_totales = self.convertir_formato_eventos(cadena_json)
        return eventos_totales


    def convertir_formato_eventos(self, cadena_json: str) -> ListaTotalDeEventos:
        '''
        Convierte la cadena json en una lista de listas de eventos
        utilizable por el programa
        '''
        eventos_json_totales = cast(EventosJSONTotales, json.loads(cadena_json))

        eventos_totales: ListaTotalDeEventos = []
        chequea(eventos_json_totales, list)
        for lista in eventos_json_totales:
            chequea(lista, list)
            eventos_ciclo: EventosDeUnCiclo = []
            for dato in lista:
                dato_tipo = dato['tipo']
                chequea(dato_tipo, int)
                tipo_evento: int = dato_tipo
                dato_dicc_evento = dato['dicc']
                chequea(dato_dicc_evento, dict)
                dicc_evento_pygame = self.crear_dicc_evento(dato_dicc_evento)
                pygame_event = pygame.event.Event(tipo_evento, dicc_evento_pygame)
                eventos_ciclo.append(pygame_event)
            eventos_totales.append(eventos_ciclo)
        return eventos_totales


    @staticmethod
    def crear_dicc_evento(dato_dicc_evento: dict[str, ValorOrigenJSON]) -> DiccEvento:
        '''
        Crea un diccionario valido para el atributo dict de un pygame Event
        '''
        dicc_evento: DiccEvento = {}
        dato_valor: ValorOrigenJSON
        k: str
        valor_dicc_pygame_event: AtributoPygameEvent
        for k, dato_valor in dato_dicc_evento.items():
            if isinstance(dato_valor, list):
                lista = dato_valor
                assert all(isinstance(x, int) for x in lista)
                if len(lista) == 2:
                    valor_dicc_pygame_event = convertir_a_tupla_dos_int(int(val) for val in lista)
                elif len(lista) == 3:
                    valor_dicc_pygame_event = convertir_a_tupla_tres_int(int(val) for val in lista)
                else:
                    raise ValueError(lista)
            elif isinstance(dato_valor, (str, int)):
                valor_dicc_pygame_event = dato_valor
            elif dato_valor is None:
                valor_dicc_pygame_event = dato_valor
            else:
                raise ValueError((k, dato_valor))
            dicc_evento[k] = valor_dicc_pygame_event
        return dicc_evento


def chequea(objeto: object, clase: type) -> None:
    '''Comprueba que es instancia en Runtime.
    En este modulo, el motivo es que estamos validando datos json externos que podrian estar corruptos'''
    if not isinstance(objeto, clase):
        raise TypeError(f'{objeto} no es instancia de {clase}')


if TYPE_CHECKING:
    from .obtenedor_eventos import ObtenedorEventos
    instancia: ObtenedorEventosJSON
    interfaz: ObtenedorEventos = instancia
