# type: ignore # non-priority

import unittest
from ...pintaformas.core.persistencia.auxiliares.analizador_num_doc import AnalizadorNumerosArchivo

class TestAnalizadorNumerosDocumento(unittest.TestCase):

    def test_obtener_mayor_numero_documento(self):
        analizador = AnalizadorNumerosArchivo()
        NOMBRES_EN_DIRECTORIO = ['un_nombre.json', 'doc_num_001.json', 'doc_num_002.json', 'doc_num_007.json', 'otro_nombre.json']
        resultado = analizador.obtener_mayor_numero_documento('doc_num_', NOMBRES_EN_DIRECTORIO)
        self.assertEqual(resultado, 7)


if __name__ == '__main__':
    unittest.main()
