import unittest
from unittest.mock import MagicMock
from ...fixtures.mocks import crear_mock_estado_herramienta

from ....pintaformas.dependencias import crear_evento_pygame, nombres_pygame
from ....pintaformas.core.general.observador_herramienta import EstadoHerramientaObservado
from ....pintaformas.core.gestor_eventos import crear_gestor_eventos
from ....pintaformas.core.control_general.realizador import Realizador
from ....pintaformas.core.control_general.variables_estado import VariableDeEstado



class TestEventoMoverRatonLlamaARealizador(unittest.TestCase):
    '''
    Comprueba la correcta comunicacion entre el GestorDeEventos y el Realizador
    cuando se mueve el raton en modo normal
    '''

    def setUp(self) -> None:
        control_general = MagicMock()
        estado_herramienta = crear_mock_estado_herramienta()
        estado_herramienta_observado = EstadoHerramientaObservado(estado_herramienta)
        realizador = Realizador(control_general, MagicMock(), estado_herramienta)
        realizador.mover_cursor = MagicMock()  # type: ignore [assignment]
        self.gestor_eventos = crear_gestor_eventos(realizador, estado_herramienta_observado)

    @unittest.skip("Desactualizado")
    def test_mover_el_raton_llama_a_metodo_mover_cursor_de_realizador(self) -> None:
        '''En modo normal, mover el ratón mueve el cursor'''
        POSICION_DESTINO = (50, 50)
        self.gestor_eventos.gestor_estado.herramienta_actual = VariableDeEstado()  # type: ignore [attr-defined] # (skipped)
        self.gestor_eventos.gestor_estado.herramienta_actual.set_valor('lapiz_libre')  # type: ignore [attr-defined] # (skipped)

        eventos = [
            crear_evento_pygame(
                nombres_pygame.MOUSEMOTION,
                dict(pos=POSICION_DESTINO)
            )
        ]
        self.gestor_eventos.incorporar_eventos(eventos)
        self.gestor_eventos.procesar_eventos()
        self.gestor_eventos.realizador.mover_cursor.assert_called_once_with(POSICION_DESTINO)  # type: ignore [attr-defined]


if __name__ == '__main__':
    unittest.main()
