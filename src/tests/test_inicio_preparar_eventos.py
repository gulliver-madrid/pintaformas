
import unittest

from ..pintaformas.inicio.operaciones_eventos.tipos import AtributoPygameEvent
from ..pintaformas.dependencias import nombres_pygame, crear_evento_pygame
from ..pintaformas.inicio.operaciones_eventos.posproceso_eventos import PostprocesadorEventos

DictPygameEvent = dict[str, AtributoPygameEvent]

DICC_MOVIMIENTO_RATON: DictPygameEvent = dict(
    pos=(44, 486), rel=(44, -61), buttons=(0, 0, 0)
)


class TestPrepararEventosParaGuardado(unittest.TestCase):

    def test_convertir_formato_eventos(self) -> None:

        lista_1 = [
            crear_evento_pygame(nombres_pygame.MOUSEMOTION, DICC_MOVIMIENTO_RATON),
            crear_evento_pygame(nombres_pygame.ACTIVEEVENT, dict(gain=1, state=1)),

        ]
        lista_2 = [
            crear_evento_pygame(nombres_pygame.KEYDOWN, dict(unicode='t', key=116, mod=0, scancode=20)),

        ]
        eventos_totales = [
        lista_1,
        lista_2,
        ]
        salida_esperada = [
            [
                {
                    'tipo': nombres_pygame.MOUSEMOTION,
                    'dicc': DICC_MOVIMIENTO_RATON
                    },
                {
                    'tipo': nombres_pygame.ACTIVEEVENT,
                    'dicc': dict(gain=1, state=1)
                    },
            ],
            [
                {
                    'tipo': nombres_pygame.KEYDOWN,
                'dicc': dict(unicode='t', key=116, mod=0, scancode=20)
                },
            ],
        ]
        posprocesador = PostprocesadorEventos(eventos_totales)
        self.assertEqual(
            posprocesador.convertir_formato_eventos(), salida_esperada
        )


if __name__ == '__main__':
    unittest.main()
