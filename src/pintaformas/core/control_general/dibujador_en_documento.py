from typing import ClassVar, Final
from ..general.doc_en_memoria import DocumentoEnMemoria
from ..elementos.formas import Circulo, Linea, BORRADO
from ..elementos.forma import Forma
from ..vista.vista import Vista


REHACER_PERMITE_INSERCION = False


class DibujadorEnDocumento:
    '''
    Dibuja en un documento provisional que despues sera convertido
    a formato .svg
    '''
    __tipos_de_forma_admitidos: ClassVar = ('circulo', 'linea', 'borrado')

    capas: Final[list[Forma]]
    siguientes: list[Forma]

    def __init__(self,
            documento_en_memoria: DocumentoEnMemoria,
            capas_vacio: list[Forma],
            vista: Vista):
        '''
        documento es una lista con el historial de comandos
        capas es una lista de los objetos dibujados
        '''
        self.capas = capas_vacio
        self.documento = documento_en_memoria
        self.vista = vista  # por ahora se encarga de esto
        self.siguientes = []  # Guarda los comandos que se anadiran con "avanzar"

    def dibuja_circulo(self,
            circulo: Circulo,
            anadir_a_documento: bool = True,
            anadir_a_capas: bool = True) -> None:
        assert self.vista.dibujador
        if anadir_a_documento:
            self.documento.append(circulo)
        if anadir_a_capas:
            self.capas.append(circulo)
        self.vista.dibujador.estampa_circulo(circulo)

    def borra_dibujo(self, anadir_a_documento: bool = True, anadir_a_capas: bool = True) -> None:
        if anadir_a_documento:
            self.documento.append(BORRADO)
        if anadir_a_capas:
            self.capas.clear()
        self.vista.dibujador.borra_dibujo()

    def reset(self) -> None:
        self.borra_dibujo()
        self.documento.clear()
        self.capas.clear()

    def dibuja_forma(self, forma: Forma, anadir_a_documento: bool = True, anadir_a_capas: bool = True) -> None:
        '''Se usa para dibujar formas sin saber a priori cuales son.'''
        tipo = forma.tipo
        if tipo == 'circulo':
            assert isinstance(forma, Circulo)
            self.dibuja_circulo(forma, anadir_a_documento, anadir_a_capas)
        elif tipo == 'linea':
            assert isinstance(forma, Linea)
            self.dibuja_linea(forma, anadir_a_documento, anadir_a_capas)
        elif tipo == 'borrado':
            self.borra_dibujo(anadir_a_documento, anadir_a_capas)
        else:
            assert tipo not in self.__tipos_de_forma_admitidos
            raise ValueError(f'Tipo de forma no reconocido: {tipo}')

    def dibuja_linea(self, linea: Linea, anadir_a_documento: bool = True, anadir_a_capas: bool = True) -> None:
        if anadir_a_documento:
            self.documento.append(linea)
        if anadir_a_capas:
            self.capas.append(linea)
        self.vista.dibujador.dibujar_linea(linea)

    def retroceder(self) -> None:
        if self.documento:
            ultimo_comando = self.documento.pop()
            self.siguientes.append(ultimo_comando)
            if ultimo_comando.tipo == 'borrado':
                self._redibujar_historial()
            else:
                assert ultimo_comando.tipo in ('circulo', 'linea')
                self.capas.pop()
                self.vista.dibujador.borra_dibujo()
                for forma in self.capas:
                    self.dibuja_forma(
                        forma, anadir_a_documento=False, anadir_a_capas=False
                    )
        else:
            print("No hay mas formas para deshacer")


    def _redibujar_historial(self) -> None:
        '''Redibuja el contenido de las capas tras deshacer un borrado'''
        # self.dibujador.borra_dibujo()
        for comando in self.documento:
            assert isinstance(comando, Forma)
            self.dibuja_forma(comando, anadir_a_documento=False)

    def redibujar_capas(self) -> None:
        for forma in self.capas:
            self.dibuja_forma(forma, anadir_a_documento=False, anadir_a_capas=False)

    def avanzar(self) -> None:
        assert not REHACER_PERMITE_INSERCION  # no se permite deshacer, anadir algo, y luego rehacer con ese algo anadido
        if self.siguientes:
            comando = self.siguientes.pop()
            self.dibuja_forma(comando)
        else:
            print("No hay mas formas para rehacer")
