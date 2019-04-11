from dataclasses import dataclass
from ...elementos.forma import Forma


@dataclass
class Documento:
    capas: list[Forma]

class DocumentoRecuperado(Documento):
    pass
