from typing import Union, TypedDict

from ...dependencias import PygameEvent
from ...core.tipos import Tuple2Int, Tuple3Int

ValorBasico = Union[str, int]
ValorOrigenJSON = Union[ValorBasico, list[int], None]
AtributoPygameEvent = Union[ValorBasico, Tuple2Int, Tuple3Int, None]

DiccEvento = dict[str, AtributoPygameEvent]

DiccionarioStrObject = dict[str, object]


class EventoJson(TypedDict):
    '''Contiene listas'''
    tipo: int
    dicc: dict[str, ValorOrigenJSON]


class EventoParaJson(TypedDict):
    '''Contiene tuplas'''
    tipo: int
    dicc: dict[str, AtributoPygameEvent]


# Los eventos JSON contienen listas en vez de tuplas
EventosJSONDeUnCiclo = list[EventoJson]
EventosJSONTotales = list[EventosJSONDeUnCiclo]

# Los eventos para JSON contienen tuplas
ListaTotalEventosParaJSON = list[list[EventoParaJson]]

EventosDeUnCiclo = list[PygameEvent]
ListaTotalDeEventos = list[EventosDeUnCiclo]
