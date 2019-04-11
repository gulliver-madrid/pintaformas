import unittest
from unittest.mock import MagicMock

from ....pintaformas.core.objetos import ObjetoVectorial
from ....pintaformas.core.tipos.cev import CodigoForma
from ....pintaformas.core.control_general.realizador import Realizador
from ....pintaformas.core.vista.capas.capa import CapaIndividual
from ....pintaformas.core.vista.areas.area_dibujo import AreaDibujo

TEXTO_CODIGO = 'forma_023'
VARIACION_Z = +1

class TestMoverFormaSeleccionadaEjeZ(unittest.TestCase):
    def _setup(self) -> None:
        control_general = MagicMock()
        self.capa_dibujo = MagicMock()
        area_dibujo = AreaDibujo(MagicMock(), MagicMock())
        area_dibujo.capas.capa_dibujo = self.capa_dibujo
        control_general.vista.areas.dibujo = area_dibujo
        self.realizador = Realizador(control_general, MagicMock(), MagicMock())

        objeto_seleccionado: ObjetoVectorial = MagicMock()
        objeto_seleccionado.codigo = CodigoForma(TEXTO_CODIGO)
        control_general.gestor_seleccion.seleccion.objeto_seleccionado = objeto_seleccionado
        self.capa_a_mover = CapaIndividual(CodigoForma(TEXTO_CODIGO))

    def test_mover_forma_seleccionada_eje_z(self) -> None:
        self._setup()
        self.capa_dibujo.capas_internas = [MagicMock(), self.capa_a_mover, MagicMock()]
        capas = self.capa_dibujo.capas_internas
        # Antes
        self.assertEqual(capas.index(self.capa_a_mover), 1)

        self.realizador.mover_forma_seleccionada_eje_z(VARIACION_Z)

        # Despues
        self.assertEqual(capas.index(self.capa_a_mover), 2)


if __name__ == '__main__':
    unittest.main()
