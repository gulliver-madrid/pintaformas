from typing import List


def ajustar_texto(texto: str, ajuste: int) -> List[str]:
    texto_en_proceso = texto
    lineas = []
    while len(texto_en_proceso) > ajuste:
        lineas.append(texto_en_proceso[:ajuste])
        texto_en_proceso = texto_en_proceso[ajuste:]
    lineas.append(texto_en_proceso)
    return lineas


def preparar_texto_para_renderizar(texto: str, ajuste: int) -> List[str]:
    if isinstance(ajuste, bool) or not isinstance(ajuste, int):
        raise Exception(f'ajuste debe ser un entero, y es {ajuste}')
    lineas_sin_ajuste = texto.split('\n')
    lineas_con_ajuste = []
    for linea_sin_ajuste in lineas_sin_ajuste:
        lineas = ajustar_texto(linea_sin_ajuste, ajuste)
        lineas_con_ajuste.extend(lineas)
    return lineas_con_ajuste
