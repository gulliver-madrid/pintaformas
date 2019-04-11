from typing import Final

from ...log_pintaformas import log, cat
from ..tipos import CodigoElementoVista, CodigoStr, codigo_to_string

class ControlDeCambios:
    __slots__=('_modificadas',)
    '''Controla los cambios en las capas para saber si renderizarlas o no'''
    _modificadas: Final[list[CodigoStr]]
    def __init__(self) -> None:
        self._modificadas = []

    def registrar(self, codigo: CodigoElementoVista) -> None:
        """Anade el codigo a la lista de modificadas si aun no estaba anotado, e incluye"""
        assert codigo != None
        codigo_str = codigo_to_string(codigo)
        if codigo_str in self._modificadas:
            return
            # log.anotar(f'Atencion: registrando codigo {codigo} ya presente en control de cambios', categoria=cat.control_cambios)
        log.anotar(f'Registrando cambio en {codigo_str}', categoria=cat.control_cambios)
        self._modificadas.append(codigo_str)

    def vaciar(self) -> None:
        self._modificadas.clear()

    def contiene(self, codigo: CodigoStr) -> bool:
        assert codigo is not None
        return codigo in self._modificadas

    def hay_cambios_pendientes(self) -> bool:
        return len(self._modificadas) > 0

    def __contains__(self, codigo: CodigoElementoVista) -> bool:
        return self.contiene(codigo_to_string(codigo))

    def debug_modificadas(self) -> frozenset[CodigoStr]:
        return frozenset(self._modificadas)
