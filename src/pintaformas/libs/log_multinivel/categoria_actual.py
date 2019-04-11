from typing import Final, Optional

from .fecha import obtener_fecha_actual


REGISTRAR_NAVEGACION_CATEGORIAS = True


class CategoriaActualLista:
    __slots__ = ('actual', '_registro')
    actual: Final[list[str]]
    _registro: Optional['Registro']

    def __init__(self) -> None:
        self._registro = Registro() if REGISTRAR_NAVEGACION_CATEGORIAS else None
        self.actual = []

    def anadir(self, categoria: str) -> None:
        self.actual.append(categoria)
        if REGISTRAR_NAVEGACION_CATEGORIAS:
            self.registrar()


    def quitar_actual(self) -> None:
        self.actual.pop()
        if REGISTRAR_NAVEGACION_CATEGORIAS:
            self.registrar()


    def registrar(self) -> None:
        entrada_registro = '.'.join(self.actual)
        if REGISTRAR_NAVEGACION_CATEGORIAS:
            assert self._registro
            self._registro.append(entrada_registro)


    def get_texto_registro(self) -> Optional[str]:
        if not REGISTRAR_NAVEGACION_CATEGORIAS:
            return None
        assert self._registro
        local_time = obtener_fecha_actual()
        texto_registro = f'\n{local_time}\nREGISTRO:\n' + self._registro.unir_con('\n')
        return texto_registro



class Registro:
    '''Guarda un registro de la navegacion por categorias. Cada item es una linea de texto que describe una categoria'''
    actual: list[str]

    def __init__(self) -> None:
        self.actual = []

    def append(self, objeto: str) -> None:
        # print(f'Llamada a registro.append({objeto})')
        self.actual.append(objeto)

    def unir_con(self, enlace: str) -> str:
        # print(f'Registro es ahora: {self.actual}')
        return enlace.join(self.actual)
