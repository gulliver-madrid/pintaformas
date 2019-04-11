from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence
from enum import auto

from ..compartido import AutoName

_NombreCategoria = str


@dataclass
class Logger:
    nombre: str
    visibles: Optional[Sequence[_NombreCategoria]] = None
    imprimir_todo: Optional[Sequence[_NombreCategoria]] = None


@dataclass
class AjustesLog:
    totales: Sequence[str]
    loggers: Sequence[Logger]


class VariacionNivel(AutoName):
    AUMENTAR = auto()
    REDUCIR = auto()
    DEJAR_IGUAL = auto()


class LogMultinivelError(RuntimeError):
    msj: str

    def __init__(self, msj: str) -> None:
        msj = poner_minuscula_inicial(msj)
        self.msj = msj
        super().__init__("Error en LogMultinivel: " + msj)

    @staticmethod
    def ruta_logs_no_indicada() -> 'LogMultinivelError':
        return LogMultinivelError(f"No se indico ruta_logs. Para silenciar por completo el log, llamar a set_config sin argumentos.")

    @staticmethod
    def ruta_logs_no_existe(ruta: Path) -> 'LogMultinivelError':
        return LogMultinivelError(f"La ruta {ruta} no existe")

    @staticmethod
    def nivel_log_menor_que_cero(nivel: int) -> 'LogMultinivelError':
        return LogMultinivelError(f"El nivel del log no puede ser menor que 0, y es {nivel}")

    @staticmethod
    def falta_nombre_categoria_aumentar_nivel() -> 'LogMultinivelError':
        return LogMultinivelError('Debe indicarse nombre de categoria al aumentar nivel')

    @staticmethod
    def modificador_no_valido(modificador: Optional[VariacionNivel]) -> 'LogMultinivelError':
        return LogMultinivelError(f'El modificador {modificador} no es valido')

    @staticmethod
    def cierre_no_valido(
        categoria_cierre: _NombreCategoria,
        categoria_actual: _NombreCategoria
    ) -> 'LogMultinivelError':
        return LogMultinivelError(f"No puede cerrarse la categoria {categoria_cierre} que no figura como abierta. La categoria actual es {categoria_actual}")

    @staticmethod
    def categoria_no_conocida(categoria: _NombreCategoria, totales: Sequence[_NombreCategoria]) -> 'LogMultinivelError':
        msj_error = f'''Categoria {categoria} no conocida'
categorias_totales={totales}'''
        return LogMultinivelError(msj_error)


def poner_minuscula_inicial(cadena: str) -> str:
    if cadena and cadena[0].isupper():
        cadena = cadena[0].lower() + cadena[1:]
    return cadena
