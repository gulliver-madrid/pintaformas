
CURSORES = ['arrow', 'diamond', 'broken_x', 'tri_left', 'tri_right']
CURSOR_SELECCION = 'diamond'



class SelectorCursor:
    def __init__(self, pygame):
        self.pygame = pygame
        self.normal = 'arrow'
        self.seleccion = CURSOR_SELECCION
        self.usando_cursor_seleccion = False


    def set_normal(self):
        self._set_cursor(self.normal)
        self.usando_cursor_seleccion = False

    def set_seleccion(self):
        self._set_cursor(self.seleccion)
        self.usando_cursor_seleccion = True


    def _set_cursor(self, nombre):
        self.pygame.mouse.set_cursor(*getattr(self.pygame.cursors, nombre))
