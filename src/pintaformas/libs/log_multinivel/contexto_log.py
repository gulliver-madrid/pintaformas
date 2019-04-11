from typing import NewType, Optional, Protocol, Type
from types import TracebackType


class LogProtocol(Protocol):
    def abrir(self, categoria: str, mensaje: str) -> None:
        ...

    def cerrar(self, categoria: Optional[str] = ..., mensaje: Optional[str] = ...) -> None:
        ...


CategoriaStr = NewType('CategoriaStr', str)
MensajeCierre = NewType('MensajeCierre', str)
MensajeApertura = NewType('MensajeApertura', str)

DatosCierre = tuple[CategoriaStr, Optional[MensajeCierre]]
DatosApertura = tuple[CategoriaStr, MensajeApertura]


class ContextoLog:
    __slots__ = ('_parent', '_pila_datos_cierre', '_datos_apertura')
    _pila_datos_cierre: list[DatosCierre]
    _datos_apertura: DatosApertura
    _parent: LogProtocol

    def __init__(self, parent: LogProtocol) -> None:
        self._parent = parent
        self._pila_datos_cierre = []

    def __enter__(self) -> None:
        self._parent.abrir(*self._datos_apertura)
        # print(f'Situacion actual del contexto: args={self.args}, args_cerrar={self.args_cerrar}')

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException], traceback: Optional[TracebackType]) -> None:
        """Reduce un nivel"""
        categoria, mensaje_cierre = self._pila_datos_cierre.pop()
        self._parent.cerrar(categoria, mensaje_cierre)
        # print(f'Situacion actual del contexto: args={self.args}, args_cerrar={self.args_cerrar}')

    def __call__(self, categoria: str, mensaje: str, *, end: Optional[str] = None) -> 'ContextoLog':
        '''end es el mensaje de cierre'''
        categoria = CategoriaStr(categoria)
        mensaje_apertura = MensajeApertura(mensaje)
        assert categoria
        if end:
            mensaje_cierre = MensajeCierre(end)
        else:
            mensaje_cierre = None
        self._pila_datos_cierre.append((categoria, mensaje_cierre))
        self._datos_apertura = (categoria, mensaje_apertura)
        return self
