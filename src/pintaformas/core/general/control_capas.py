from typing import ClassVar, Generic, Protocol, TypeVar

from ..objetos import ObjetoVectorial
from ..tipos.cev import CodigoElementoVista, CodigoStr, codigo_to_string
from ..vista.objeto_con_surface import ObjetoConSurface
from .control_cambios import ControlDeCambios


class ControlObjetosVista:
    # TODO: Revisar si solo se refiere a la vista, y en funcion de eso corregir el nombre o ubicar en la estructura de la vista
    """
    Solo este objeto puede acceder directamente al DiccionarioCapas y el DiccionarioObjetos
    """

    def __init__(self) -> None:
        self._diccionario_capas = DiccionarioCapas()
        self._diccionario_objetos = DiccionarioObjetos()

    def anadir_binomio(self, objeto: ObjetoVectorial, capa: ObjetoConSurface) -> None:
        self._diccionario_objetos.add_item(objeto)
        self._diccionario_capas.add_item(capa)

    def get_capa(self, codigo: CodigoElementoVista) -> ObjetoConSurface:
        return self._diccionario_capas.get_item(codigo)

    def get_capa_by_codigo_str(self, codigo_str: CodigoStr) -> ObjetoConSurface:
        return self._diccionario_capas.get_item_by_codigo_str(codigo_str)

    def anadir_capa(self, capa: ObjetoConSurface) -> None:
        self._diccionario_capas.add_item(capa)

    def anadir_objeto_vectorial(self, objeto: ObjetoVectorial) -> None:
        self._diccionario_objetos.add_item(objeto)

    def get_diccionario_objetos_para_renderizador(self) -> 'MappingToObjetosParaRenderizador':
        return self._diccionario_objetos

class MappingToObjetosParaRenderizador(Protocol):
    def get_item(self, key: CodigoElementoVista) -> ObjetoVectorial:
        ...

class ControlDeCapas:
    def __init__(self, control_cambios: ControlDeCambios):
        self.control_cambios = control_cambios
        self.control_objetos_vista = ControlObjetosVista()


T = TypeVar('T', ObjetoConSurface, ObjetoVectorial)


class DiccionarioPorCodigo(Generic[T]):
    nombre: ClassVar[str]
    data: dict[CodigoStr, T]

    def __init__(self) -> None:
        self.data = {}

    def add_item(self, item: T) -> None:
        codigo = item.codigo
        self._add_pair(codigo, item)

    def add_pair(self, key: CodigoElementoVista, value: T) -> None:
        self._add_pair(key, value)

    def get_item(self, key: CodigoElementoVista) -> T:
        return self.data[codigo_to_string(key)]

    def get_item_by_codigo_str(self, key: CodigoStr) -> T:
        return self.data[key]

    def _add_pair(self, key: CodigoElementoVista, value: T) -> None:
        code_str: CodigoStr = codigo_to_string(key)
        self.data[code_str] = value



class DiccionarioCapas(DiccionarioPorCodigo[ObjetoConSurface]):
    nombre = 'diccionario_capas'


class DiccionarioObjetos(DiccionarioPorCodigo[ObjetoVectorial]):
    nombre = 'diccionario_objetos'
