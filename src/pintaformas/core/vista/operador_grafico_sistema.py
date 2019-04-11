import pygame

from ...core.vista.surfaces import GenericSurface, GenericSurfaceFactory
from ...dependencias import PygameRect



class OperadorGraficoSistema:
    """Maneja las operaciones que interactuan graficamente con el sistema"""
    __slots__ = 'surface_factory'
    surface_factory: GenericSurfaceFactory

    def __init__(self, surface_factory: GenericSurfaceFactory):
        self.surface_factory = surface_factory

    def actualizar_pantalla(self, *args: PygameRect) -> None:
        pygame.display.update(*args)

    def mostrar_cursor_sistema_operativo(self, valor: bool) -> None:
        pygame.mouse.set_visible(valor)

    def obtener_surface_principal(self) -> GenericSurface:
        return self.surface_factory.from_surface(pygame.display.get_surface())

    def obtener_subsurface_ventana(self, rect: PygameRect) -> GenericSurface:
        surface_principal = self.obtener_surface_principal()
        return surface_principal.subsurface(rect)

    def poner_titulo(self, titulo: str) -> None:
        pygame.display.set_caption(titulo)
