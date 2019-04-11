from typing import Optional



class InfoGuardadoDocumento:
    def __init__(self, documento_normalizado: dict[str, object], nombre_proporcionado: Optional[str] = None):
        self.documento_normalizado = documento_normalizado
        self.nombre_proporcionado = nombre_proporcionado

    def extraer(self) -> tuple[object, Optional[str]]:
        return (self.documento_normalizado, self.nombre_proporcionado)
