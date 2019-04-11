import unittest

from ....pintaformas.core.tipos import CodigoAreaPF, CodigoElementoVista, CodigoForma, CodigoObjetoEspecial
from ....pintaformas.core.general.control_cambios import ControlDeCambios
from ....pintaformas.core.vista.revisador_arbol import RevisadorArbol
from ....pintaformas.core.vista.capas import Capa, CapaContenedora


class TestRevisarArbol(unittest.TestCase):

    def _setup(self) -> None:
        """Uso un setup manual para hacer los tests compatibles con hammett"""
        self.capa_dibujo = self.crear_capa_contenedora(CodigoObjetoEspecial.dibujo)
        capa_forma_001 = self.crear_mock_capa(CodigoForma('forma_001'))
        self.capa_dibujo.capas_internas = [capa_forma_001]
        self.control_cambios = ControlDeCambios()
        self.revisador_arbol = RevisadorArbol(self.control_cambios)


    @staticmethod
    def crear_mock_capa(codigo: CodigoElementoVista) -> Capa:
        capa = Capa(codigo)
        return capa

    @staticmethod
    def crear_capa_contenedora(codigo: CodigoElementoVista) -> CapaContenedora:
        capa = CapaContenedora(codigo)
        return capa

    def crear_area_dibujo_con_contenido(self) -> CapaContenedora:
        area_dibujo = self.crear_capa_contenedora(CodigoAreaPF.area_dibujo)
        capa_cursor = self.crear_mock_capa(CodigoObjetoEspecial.cursor)
        area_dibujo.capas_internas = [self.capa_dibujo, capa_cursor]
        return area_dibujo

    def test_revisar_arbol_desde_capa_dibujo(self) -> None:
        '''Testa un caso sencillo'''
        self._setup()
        self.control_cambios.registrar(CodigoForma('forma_001'))
        resultado = self.revisador_arbol.revisar_arbol(self.capa_dibujo)
        resultado_esperado = ['forma_001', 'dibujo']
        self.assertEqual(resultado, resultado_esperado)


    def test_revisar_arbol_desde_area_dibujo(self) -> None:
        '''Testa un caso un poco mas complejo'''
        self._setup()
        area_dibujo = self.crear_area_dibujo_con_contenido()
        self.control_cambios.registrar(CodigoObjetoEspecial.cursor)
        self.control_cambios.registrar(CodigoForma('forma_001'))
        resultado = self.revisador_arbol.revisar_arbol(area_dibujo)
        resultado_esperado = ['forma_001', 'dibujo', 'cursor', 'area_dibujo']
        self.assertEqual(resultado, resultado_esperado)

    def test_revisar_arbol_caso_zoom(self) -> None:
        '''Testa un caso un poco mas complejo (caso_zoom)'''
        self._setup()
        area_dibujo = self.crear_area_dibujo_con_contenido()
        self.control_cambios.registrar(CodigoObjetoEspecial.visualizacion)
        resultado = self.revisador_arbol.revisar_arbol(area_dibujo)
        resultado_esperado = ['forma_001', 'dibujo', 'cursor', 'area_dibujo']
        self.assertEqual(resultado, resultado_esperado)

    def test_revisar_arbol_caso_zoom_tres_formas(self) -> None:
        '''Testa un caso un poco mas complejo (caso_zoom_tres_formas)'''
        self._setup()
        area_dibujo = self.crear_area_dibujo_con_contenido()
        capa_forma_002 = self.crear_mock_capa(CodigoForma('forma_002'))
        capa_forma_003 = self.crear_mock_capa(CodigoForma('forma_003'))
        capa_contenedora_interna = area_dibujo.capas_internas[0]
        assert isinstance(capa_contenedora_interna, CapaContenedora)
        capa_contenedora_interna.capas_internas.extend([capa_forma_002, capa_forma_003])
        # print('EN EL TEST')
        # print(f'{area_dibujo.capas_internas[0].codigo}')
        # print(f'{area_dibujo.capas_internas[0].capas_internas}')
        # print()
        self.control_cambios.registrar(CodigoObjetoEspecial.visualizacion)
        resultado = self.revisador_arbol.revisar_arbol(area_dibujo)
        resultado_esperado = ['forma_001', 'forma_002', 'forma_003', 'dibujo', 'cursor', 'area_dibujo']
        self.assertEqual(resultado, resultado_esperado)



if __name__ == '__main__':
    unittest.main()
