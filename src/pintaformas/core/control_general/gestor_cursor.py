from ...log_pintaformas import log, cat
from ..elementos.cursor import Cursor, TipoCursor
from ..tipos import PosicionEnPantalla


class GestorCursor:

    def __init__(self, cursor: Cursor):
        self.cursor = cursor
        self._visible = True

    def establecer_tipo_de_cursor(self, tipo: TipoCursor) -> None:
        '''Este sera el tipo de cursor que se vera mientras estemos en el area de dibujo'''
        log.anotar(f'establecer_tipo_de_cursor({tipo.value})', cat.cursor)
        self.cursor.tipo_cursor = tipo


    def ocultar_cursor(self) -> None:
        self.cursor.borra_cursor_manual()
        # self.cursor.set_visibilidad_cursor_so(True)


    def usar_cursor_dibujo(self, valor: bool) -> None:
        '''Si es True, utiliza el cursor de dibujo disponible'''
        if valor and self.cursor.tipo_cursor != TipoCursor.flecha:
            self.cursor.set_visibilidad_cursor_so(False)
            self.cursor.muestra_cursor_manual()
        else:
            self.cursor.borra_cursor_manual()
            self.cursor.set_visibilidad_cursor_so(True)

    def mover_cursor(self, posicion: PosicionEnPantalla) -> None:
        '''Gestiona el movimiento normal del cursor'''
        self.cursor.mover_cursor_a_posicion(posicion)
