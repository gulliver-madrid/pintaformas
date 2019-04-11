from ..core.ajustes_generales import AjustesGenerales
from ..core import cfg

cfg.FPS = 30


AJUSTES_PREDETERMINADOS: AjustesGenerales = AjustesGenerales(
    dimensiones=cfg.DIMENSIONES_VENTANA,
    fps=cfg.FPS,
    titulo=cfg.NOMBRE_PROGRAMA,
    cargar_dibujo_guardado=True,
    nombre_documento_proporcionado_por_el_usuario=None,
    grabar_dibujo_al_salir=True,
    usar_persistencia=True,
    grabar_eventos=False,
    eventos_a_cargar=None,
)
