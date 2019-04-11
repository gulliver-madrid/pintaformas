import unittest

from ...pintaformas.inicio.operaciones_eventos.posproceso_eventos import PostprocesadorEventos
from ...pintaformas.inicio.operaciones_eventos.obtenedor_eventos_json import ObtenedorEventosJSON



class TestInstanciarObjetos(unittest.TestCase):

    def test_instanciar_obtenedor_eventos_json(self) -> None:
        obtenedor_eventos_json = ObtenedorEventosJSON("{}", carga_automatica=False)
        assert obtenedor_eventos_json

    def test_instanciar_postprocesador(self) -> None:
        postprocesador = PostprocesadorEventos([])
        assert postprocesador
