
from ..core.ajustes_generales import AjustesGenerales


class ValidadorAjustesUsuario:
    def __init__(self, ajustes_usuario: AjustesGenerales, ajustes_generales: AjustesGenerales) -> None:
        self.ajustes_usuario = ajustes_usuario
        self.ajustes_generales = ajustes_generales

    def validar(self) -> None:
        usuario = self.ajustes_usuario
        generales = self.ajustes_generales
        no_registrados = set(usuario).difference(generales)
        if no_registrados:
            texto = self._generar_texto_error(no_registrados)
            raise RuntimeError(texto)

    def _generar_texto_error(self, erroneos: set[str]) -> str:
        nombres = sorted(erroneos)
        assert nombres
        if len(nombres) == 1:
            nombre = nombres[0]
            return f'El ajuste {nombre} no esta registrado'
        nombres_str = ", ".join(nombres)
        return f'Los ajustes {nombres_str} no estan registrados'
