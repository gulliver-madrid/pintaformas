import time

from ..log_pintaformas import log, cat

NUM_DECIMALES = 2


def imprimir_ciclo_en_log(tiempo_inicial: float, num_ciclo: int) -> None:
    texto_ciclo = '\n'.join(
        [f'\n\nCiclo: {num_ciclo}', '.' * 8]
    )
    log.anotar(texto_ciclo)
    log.anotar(
        f'Tiempo actual: {round(time.time() - tiempo_inicial, NUM_DECIMALES)}',
        categoria=cat.mostrar_tiempo
    )


NOMBRES_AJUSTES_PERSISTENCIA = (
    'cargar_dibujo_guardado',
    'nombre_documento_proporcionado_por_el_usuario',
    'grabar_dibujo_al_salir'
)
