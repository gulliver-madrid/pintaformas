from typing import NoReturn

from ....log_pintaformas import log, cat
from ...tipos import Vector2D, CodigoObjetoEspecial
from ..tipos import GestorEventosPFTecladoBase
from ..excepciones_eventos import EndInput, EventoUsado

COEFICIENTE_ZOOM = 1.15


class GestorEventosTecladoUniversal(GestorEventosPFTecladoBase):
    '''
    Gestiona los eventos del teclado cuando esta activada cualquier herramienta
    '''

    def init(self) -> None:
        self.equivalencias = {
            '1': self.aumentar_zoom,
            '2': self.reducir_zoom,
            '3': lambda: self.mover_forma_seleccionada_eje_z(1),
            '4': lambda: self.mover_forma_seleccionada_eje_z(-1),
            'l': self.desplazar_fondo_a_izquierda,
            'h': self.desplazar_fondo_a_derecha,
            'j': self.desplazar_fondo_arriba,
            'k': self.desplazar_fondo_abajo,
            'm': self.crear_marca,
            'd': lambda: breakpoint(),
            'b': self.borrar_dibujo,
            'r': self.resetear,
            ('z', 'control'): self.realizador.dibujador_en_documento.retroceder,
            ('z', 'shift', 'control'): self.realizador.dibujador_en_documento.avanzar,
            'escape': self.realizador.salir,
        }
        self.numero_marca = 1

    def borrar_dibujo(self) -> NoReturn:
        self.realizador.dibujador_en_documento.borra_dibujo()
        raise EventoUsado()


    def aumentar_zoom(self) -> NoReturn:
        self.realizador.cambiar_zoom(COEFICIENTE_ZOOM)
        raise EventoUsado()

    def reducir_zoom(self) -> NoReturn:
        self.realizador.cambiar_zoom(1 / COEFICIENTE_ZOOM)
        raise EventoUsado()

    def desplazar_fondo_a_derecha(self) -> None:
        self._desplazar_fondo(Vector2D((-50, 0)))

    def desplazar_fondo_a_izquierda(self) -> None:
        self._desplazar_fondo(Vector2D((50, 0)))

    def desplazar_fondo_arriba(self) -> None:
        self._desplazar_fondo(Vector2D((0, 50)))


    def desplazar_fondo_abajo(self) -> None:
        self._desplazar_fondo(Vector2D((0, -50)))


    def _desplazar_fondo(self, desplazamiento: Vector2D) -> NoReturn:
        self.realizador.visualizacion.desplazar(desplazamiento)
        self.realizador.control_cambios.registrar(CodigoObjetoEspecial.visualizacion)
        raise EventoUsado()


    def mover_forma_seleccionada_eje_z(self, variacion: int) -> None:
        if self.realizador.gestor_seleccion.seleccion.objeto_seleccionado:
            self.realizador.mover_forma_seleccionada_eje_z(variacion)
        else:
            print('No hay ninguna forma seleccionada')


    def crear_marca(self) -> NoReturn:
        '''Crea una marca en el log'''
        log.anotar(f'MARCA NUMERO {self.numero_marca}', categoria=cat.crear_marca)
        self.numero_marca += 1
        raise EventoUsado()

    def resetear(self) -> NoReturn:
        entrada = input('Atención: has solicitado resetear. Esto borrará el dibujo actual. ¿Estás seguro? s/N?')
        print(f"{entrada=}")
        if entrada.lower() == 's':
            print("Reseteo activado")
            self.realizador.dibujador_en_documento.reset()
        else:
            print('Se abortó el reseteo')
        raise EndInput()

