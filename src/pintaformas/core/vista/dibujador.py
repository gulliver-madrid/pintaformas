from ...log_pintaformas import log
from .. import cfg
from ..elementos.cursor import Cursor
from ..elementos.formas import Circulo, Linea
from ..general.control_capas import ControlDeCapas
from ..tipos import Color, Dimensiones
from .capas import CapaContenedora, CapaIndividual
from .visualizacion import Visualizacion


class DibujadorAreaDibujo:
    '''
    Esta clase se encarga de generar los datos de visualizacion de los diferentes elementos.
    (A excepcion del zoom y el desplazamiento, que se determinan por el renderizador
    en el momento del renderizado.)
    '''

    def __init__(self,
            dimensiones_area_dibujo: Dimensiones,
            visualizacion: Visualizacion,
            capa_dibujo: CapaContenedora,
            capa_cursor: CapaIndividual,
            capa_seleccion: CapaIndividual,
            control_capas: ControlDeCapas):
        self.dimensiones_area_dibujo = dimensiones_area_dibujo
        self.visualizacion = visualizacion
        self.capa_dibujo = capa_dibujo
        self.capa_cursor = capa_cursor
        self.capa_seleccion = capa_seleccion
        self.color_transparente = cfg.COLOR_TRANSPARENTE
        self.control_cambios = control_capas.control_cambios
        self.control_objetos_vista = control_capas.control_objetos_vista

    def cambiar_color_pluma(self) -> None:
        pass


    def estampa_circulo(self, circulo: Circulo) -> None:
        '''Estampa un circulo relleno'''
        capa_circulo = CapaIndividual(circulo.codigo, 'circulo')
        self.control_objetos_vista.anadir_binomio(circulo, capa_circulo)
        self.capa_dibujo.anadir_capa(capa_circulo)
        log.anotar(f'Dibujado circulo con codigo {circulo.codigo}')
        self.control_cambios.registrar(capa_circulo.codigo)


    def borra_dibujo(self) -> None:
        assert self.capa_dibujo.surface
        self.capa_dibujo.surface.fill(Color(cfg.COLOR_TRANSPARENTE))
        self.capa_dibujo.capas_internas.clear()
        self.control_cambios.registrar(self.capa_dibujo.codigo)


    def borra_cursor(self) -> None:
        codigo = self.capa_cursor.codigo
        cursor = self.control_objetos_vista.get_capa(codigo)
        # TODO: revisar este narrowing
        assert isinstance(cursor, Cursor)
        cursor.borra_cursor_manual()
        self.control_cambios.registrar(self.capa_cursor.codigo)


    def dibujar_linea(self, linea: Linea) -> None:
        '''Como trazo, pero recibe un objeto linea'''
        # self.trazo(linea.origen, linea.destino, linea.color)
        # capa_trazo = CapaTrazo(color, origen, destino)
        capa_linea = CapaIndividual(linea.codigo, 'linea')
        self.control_objetos_vista.anadir_binomio(linea, capa_linea)
        self.capa_dibujo.anadir_capa(capa_linea)
        self.control_cambios.registrar(capa_linea.codigo)
