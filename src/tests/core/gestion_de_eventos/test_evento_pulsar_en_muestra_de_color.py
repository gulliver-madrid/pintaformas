import unittest
from unittest.mock import MagicMock

from ...fixtures.mocks import crear_mock_control_general, crear_mock_estado_herramienta, crear_mock_vista


from ....pintaformas.dependencias import crear_evento_pygame, PygameRect, nombres_pygame
from ....pintaformas.core.elementos.herramienta import Herramienta
from ....pintaformas.core.tipos import Color
from ....pintaformas.core.general.observador_herramienta import EstadoHerramientaObservado
from ....pintaformas.core.control_general.realizador import Realizador
from ....pintaformas.core.gestor_eventos import crear_gestor_eventos


class TestEventoPulsarMuestraColoresLlamaARealizador(unittest.TestCase):
    '''
    Comprueba la correcta comunicacion entre el GestorDeEventos y el Realizador
    cuando se pulsa en una muestra de color.
    '''

    def setUp(self) -> None:
        self.vista = crear_mock_vista()
        control_general = crear_mock_control_general()
        control_general.vista = self.vista
        estado_herramienta = crear_mock_estado_herramienta()
        estado_herramienta_observado = EstadoHerramientaObservado(estado_herramienta)
        self.realizador = Realizador(control_general, MagicMock(), estado_herramienta)
        self.realizador.seleccionar_color = MagicMock() # type: ignore [assignment]
        self.gestor_eventos = crear_gestor_eventos(self.realizador, estado_herramienta_observado)


    def test_pulsar_muestra_colores_llama_a_metodo_seleccionar_color_de_realizador(self) -> None:
        '''Al pulsar en una posicion que coincide con un rect de muestra de color,
        se llama a seleccionar ese color'''
        # Preparar
        POSICION_PULSADA = (600, 500)

        RECT_OBJETIVO = PygameRect(590, 490, 20, 20)
        OTRO_RECT = PygameRect(0, 0, 10, 10)
        assert RECT_OBJETIVO.collidepoint(POSICION_PULSADA)

        COLOR_ESPERADO = Color((255, 128, 0))
        OTRO_COLOR = Color((0,0,0))

        rects_colores = [OTRO_RECT, OTRO_RECT, RECT_OBJETIVO, OTRO_RECT]
        colores = [OTRO_COLOR, OTRO_COLOR, COLOR_ESPERADO, OTRO_COLOR]

        self.realizador.cambiar_herramienta(Herramienta.lapiz_libre)
        self.vista.areas.muestras_colores.rects_colores = rects_colores
        self.vista.areas.muestras_colores.colores_muestras = colores

        eventos = [
            crear_evento_pygame(
                nombres_pygame.MOUSEBUTTONDOWN,
                dict(pos=POSICION_PULSADA)
            )
        ]

        # Actuar
        self.gestor_eventos.incorporar_eventos(eventos)
        self.gestor_eventos.procesar_eventos()

        # Afirmar
        self.realizador.seleccionar_color.assert_called_once_with(COLOR_ESPERADO) # type: ignore [attr-defined]





if __name__ == '__main__':
    unittest.main()
