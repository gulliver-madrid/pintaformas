
from ...log_pintaformas import log
from ..tipos import Color, PosicionEnDocumento, PosicionEnPantalla, Desplazamiento, TuplaDosEnteros
from ..elementos.formas import Circulo
from ..elementos.seleccion import Seleccion
from ..general.control_cambios import ControlDeCambios
from ..vista.vista import Vista
from ..vista.visualizacion import Visualizacion


VARIACION_RADIO = 10


class GestorSeleccionCirculo:
    __slots__ = ('visualizacion', 'seleccion', 'control_cambios', 'color_pluma', 'posicion_inicial_circulo')
    visualizacion: Visualizacion
    seleccion: Seleccion
    control_cambios: ControlDeCambios
    color_pluma: Color
    posicion_inicial_circulo: PosicionEnDocumento


    def __init__(self, seleccion: Seleccion, vista: Vista, control_cambios: ControlDeCambios):
        self.visualizacion = vista.visualizacion
        self.seleccion = seleccion
        self.control_cambios = control_cambios


    def _comprueba_nada_seleccionado(self) -> None:
        assert not self.seleccion.objeto_seleccionado, f'{self.seleccion.objeto_seleccionado}'


    def crea_circulo(self, posicion_en_pantalla: PosicionEnPantalla) -> None:
        '''Crea un circulo y lo selecciona'''
        RADIO_MINIMO = 1
        log.anotar('Creando circulo en GestorSeleccion')
        centro_en_documento = self.visualizacion.pasar_a_documento(posicion_en_pantalla)
        self.posicion_inicial_circulo = centro_en_documento
        self.seleccion.objeto_seleccionado = Circulo(self.color_pluma, centro_en_documento, RADIO_MINIMO)


    def modifica_circulo_recien_creado(self, posicion_en_pantalla: PosicionEnPantalla) -> None:
        circulo = self.seleccion.objeto_seleccionado
        assert isinstance(circulo, Circulo)
        punto_de_partida_documento = self.posicion_inicial_circulo
        posicion_en_documento = self.visualizacion.pasar_a_documento(posicion_en_pantalla)
        movimiento_relativo = Desplazamiento(posicion_en_documento.restar(punto_de_partida_documento))
        direccion_desplazamiento = TuplaDosEnteros((mov > 0) - (mov < 0) for mov in movimiento_relativo)
        desplamientos_absolutos = [abs(movimiento) for movimiento in movimiento_relativo]
        max_desplazamiento = max(desplamientos_absolutos)

        if max_desplazamiento >= 2:
            radio_en_documento = max_desplazamiento
            desplazamiento_aplicado = Desplazamiento(radio_en_documento * signo for signo in direccion_desplazamiento)
            centro_en_documento = PosicionEnDocumento(punto_de_partida_documento.sumar(desplazamiento_aplicado))

            circulo.posicion = centro_en_documento
            circulo.radio = radio_en_documento

        self.control_cambios.registrar(self.seleccion.codigo)


    def mover_circulo(self, posicion_pantalla: PosicionEnPantalla) -> None:
        '''Mueve un circulo seleccionado'''
        circulo = self.seleccion.objeto_seleccionado
        assert isinstance(circulo, Circulo)
        circulo.posicion = self.visualizacion.pasar_a_documento(posicion_pantalla)
        self.control_cambios.registrar(self.seleccion.codigo)


    def modificar_circulo(self, direccion: str) -> None:
        '''Modifica el tamano o color del circulo seleccionado'''
        circulo = self.seleccion.objeto_seleccionado
        assert isinstance(circulo, Circulo)
        # Cambiar radio
        if direccion in ['arriba']:
            circulo.radio += VARIACION_RADIO
        elif direccion in ['abajo']:
            circulo.radio -= VARIACION_RADIO
        self.control_cambios.registrar(self.seleccion.codigo)



    def deseleccionar(self) -> None:
        self.seleccion.objeto_seleccionado = None
