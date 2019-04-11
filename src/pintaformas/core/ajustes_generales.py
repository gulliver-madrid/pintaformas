from typing import Literal, Optional, TypedDict

from ..core.tipos import Tuple2Int

CLAVES_PERMITIDAS_EN_AJUSTES_GENERALES = Literal[
    'dimensiones',
    'fps',
    'titulo',
    'cargar_dibujo_guardado',
    'nombre_documento_proporcionado_por_el_usuario',
    'grabar_dibujo_al_salir',
    'usar_persistencia',
    'grabar_eventos',
    'eventos_a_cargar'
]

class AjustesGenerales(TypedDict, total=False):
    dimensiones: Tuple2Int
    fps: int
    titulo: str
    cargar_dibujo_guardado: bool
    nombre_documento_proporcionado_por_el_usuario: Optional[str]
    grabar_dibujo_al_salir: bool
    usar_persistencia: bool
    grabar_eventos: bool
    eventos_a_cargar: Optional[str]
