from typing import Optional, NoReturn

from ...log_pintaformas import log, cat
from ...core.vista.surfaces import GenericSurface
from .. import cadenas
from ..tipos.cev import LIENZO_DIBUJO_SELECCION, CodigoObjetoEspecial
from ..excepciones import SalirApp
from ..elementos.cursor import TipoCursor
from ..objetos import ObjetoVectorial, Objeto
from ..tipos import CodigoForma, Color, PosicionEnPantalla, PosicionEnPantallaRelativa, convertir_a_tupla_dos_int
from ..elementos.forma import Forma
from ..elementos.formas import Circulo
from ..vista.capas.capa import CapaIndividual
from ..vista.areas.area_dibujo import AreaDibujo
from ..vista.visualizacion import Visualizacion
from ..general.control_cambios import ControlDeCambios
from ..elementos.herramienta import HERRAMIENTAS, Herramienta
from .control_general import ControlGeneral
from .estado_herramienta import EstadoHerramienta
from .lapiz import Lapiz

X, Y = 0, 1

HERRAMIENTAS_CURSOR_PINTURA = (Herramienta.lapiz_libre, Herramienta.recta, Herramienta.circulo)
COLOR_SELECCIONADO_INICIAL = (0, 0, 0)


class NuevoEstado:
    '''
    Conserva valores para uso unicamente del realizador
    '''

    def __init__(self) -> None:
        self.color_seleccionado: Optional[Color] = None



class Realizador(Objeto):
    def __init__(self,
            control_general: ControlGeneral,
            control_cambios: ControlDeCambios,
            estado_herramienta: EstadoHerramienta):
        self.control_general = control_general
        self.vista = control_general.vista
        self.dibujador_en_documento = control_general.dibujador_en_documento
        self.gestor_seleccion = control_general.gestor_seleccion
        self.gestor_seleccion_circulo = control_general.gestor_seleccion_circulo
        self.gestor_cursor = control_general.gestor_cursor
        self.control_cambios = control_cambios
        self.estado_herramienta = estado_herramienta
        self.visualizacion: Visualizacion = self.vista.visualizacion
        self.lapiz = Lapiz(
            self.vista.visualizacion,
            self.dibujador_en_documento,
            self.gestor_seleccion
        )
        self.nuevo_estado = NuevoEstado()


    def mover_cursor(self, posicion: PosicionEnPantalla) -> None:
        self.control_general.gestor_cursor.mover_cursor(posicion)
        self.mostrar_cursor_en_pantalla(posicion)

    def set_ocultamiento_cursor_mientras_se_dibuja(self, valor: bool) -> None:
        if valor:
            self.control_general.gestor_cursor.ocultar_cursor()
        else:
            posicion = self.control_general.gestor_cursor.cursor.posicion
            self.mostrar_cursor_en_pantalla(posicion)
        self.control_cambios.registrar(CodigoObjetoEspecial.cursor)

    def mostrar_cursor_en_pantalla(self, posicion: PosicionEnPantalla) -> None:
        log.anotar(f'mostrar_cursor_en_pantalla: {posicion}')
        separacion_vertical = self.vista.separacion_vertical
        posicion_vertical = posicion[Y]
        if (
            (posicion_vertical > separacion_vertical) and
            (self.control_general.gestor_cursor.cursor.visibilidad_cursor_manual == True)
            ):
            self.control_general.gestor_cursor.usar_cursor_dibujo(False)

        elif (posicion_vertical < separacion_vertical):
            self.control_general.gestor_cursor.usar_cursor_dibujo(True)
        self.control_cambios.registrar(CodigoObjetoEspecial.cursor)

    def set_visibilidad_general_cursor(self, valor: bool) -> None:
        if valor:
            posicion_cursor = self.control_general.gestor_cursor.cursor.posicion
            self.mostrar_cursor_en_pantalla(posicion_cursor)
        else:
            self.control_general.gestor_cursor.ocultar_cursor()
            self.control_cambios.registrar(CodigoObjetoEspecial.cursor)

    def seleccionar_color(self, color: Color) -> None:
        log.anotar(f'Nuevo color: {color}')
        self.nuevo_estado.color_seleccionado = color
        self.control_general.gestor_cursor.cursor.color = color
        self.gestor_seleccion.color_pluma = color
        self.gestor_seleccion_circulo.color_pluma = color
        area_color_seleccionado = self.vista.areas.color_seleccionado
        area_color_seleccionado.color_seleccionado = color
        self.control_cambios.registrar(area_color_seleccionado.codigo)

    def establece_valores_iniciales(self) -> None:
        estado_inicial = Herramienta.seleccion
        self.cambiar_herramienta(estado_inicial)
        self.seleccionar_color(Color(COLOR_SELECCIONADO_INICIAL))


    def estampar_circulo(self) -> None:
        circulo = self.gestor_seleccion.seleccion.objeto_seleccionado
        assert isinstance(circulo, Circulo)
        assert circulo.tipo == 'circulo'
        assert hasattr(circulo, 'posicion')
        self.dibujador_en_documento.dibuja_circulo(circulo)
        self.gestor_seleccion.deseleccionar()

    def redimensionar_contenido_ventana(self) -> None:
        '''
        Cuando el usuario redimensiona la ventana, la surface principal es la misma,
        pero cambia su tamano.
        Aqui se trata de actualizar los parametros del programa para que se adapte a
        las nuevas dimensiones.
        '''
        self.vista.creador_capas.creador_rects_areas.borrar_referencias_clave()
        dicc_areas = self.vista.dicc_areas
        self.vista.creador_capas.creador_rects_areas.anadir_rects(dicc_areas)
        for area in dicc_areas.values():
            area.surface = None  # De no aplicarse, se genera un fallo de memoria un poco mas adelante
            self.control_cambios.registrar(area.codigo)
        for codigo in LIENZO_DIBUJO_SELECCION:
            self.control_cambios.registrar(codigo)



    def finalizar_segmento_recta(self, posicion: PosicionEnPantalla) -> None:
        if self.lapiz.trazo_iniciado:
            self.gestor_seleccion.seleccion.objeto_seleccionado = None  # Para que nos deje proceder
            self.lapiz.finalizar_trazo(posicion)
            self.control_cambios.registrar(CodigoObjetoEspecial.seleccion)
        else:
            raise Exception('No hay un trazo iniciado')

    def abandonar_recta(self) -> None:
        if self.lapiz.trazo_iniciado:
            self.lapiz.trazo_iniciado = None
            self.gestor_seleccion.deseleccionar()
            self.control_cambios.registrar(CodigoObjetoEspecial.seleccion)


    def seleccionar_herramienta(self, i: int) -> None:
        self.cambiar_herramienta(HERRAMIENTAS[i])


    def cambiar_herramienta(self, nueva_herramienta: Herramienta) -> None:
        self.estado_herramienta.valor = nueva_herramienta
        indice_herramienta = HERRAMIENTAS.index(nueva_herramienta)
        area_herramientas = self.vista.areas.herramientas
        area_herramientas.set_indice_herramienta(indice_herramienta)
        if nueva_herramienta in HERRAMIENTAS_CURSOR_PINTURA:
            self.control_general.gestor_cursor.establecer_tipo_de_cursor(TipoCursor.pintura)
        else:
            self.control_general.gestor_cursor.establecer_tipo_de_cursor(TipoCursor.flecha)
        self.control_cambios.registrar(area_herramientas.codigo)
        self.control_cambios.registrar(CodigoObjetoEspecial.cursor)

        area_informativa = self.vista.areas.informativa
        if nueva_herramienta != area_informativa.herramienta:
            log.anotar(f'Realizador: cambiando herramienta en area_informativa a {nueva_herramienta}')
            area_informativa.registrar_cambio_herramienta(nueva_herramienta)
            self.control_cambios.registrar(area_informativa.codigo)
        log.anotar(f'Elegida la herramienta {nueva_herramienta}', cat.cambio_herramienta)


    def mover_forma_seleccionada_eje_z(self, variacion: int) -> None:
        assert variacion in (-1, 1)
        objeto_seleccionado = self.gestor_seleccion.seleccion.objeto_seleccionado
        assert objeto_seleccionado
        codigo = objeto_seleccionado.codigo
        assert isinstance(codigo, CodigoForma), codigo
        area_dibujo = self.vista.areas.dibujo
        assert isinstance(area_dibujo, AreaDibujo), area_dibujo
        capas = area_dibujo.capas.capa_dibujo.capas_internas
        for capa in capas:
            if capa.codigo == codigo:
                indice = capas.index(capa)
                capas.pop(indice)
                capas.insert(indice + variacion, capa)
                break
        self.control_cambios.registrar(CodigoObjetoEspecial.dibujo)

    def seleccionar_por_posicion(self, posicion: PosicionEnPantalla) -> None:
        '''
        Selecciona la forma coincidente con la posicion que se encuentre mas
        arriba en el eje Z.
        Si la forma ya estaba seleccionada, se deselecciona, y si se hace click
        en un espacio vacio de formas, se deselecciona la que estuviera seleccionada
        '''
        capa_clicada = self._obtener_capa_clicada(posicion)
        if capa_clicada:
            objeto_en_capa = self.vista.diccionario_objetos.get_item(capa_clicada.codigo)
            seleccion = self.gestor_seleccion.seleccion
            if seleccion.objeto_seleccionado == objeto_en_capa:
                seleccion.objeto_seleccionado = None
            else:
                self.seleccionar(capa_clicada)
                self._log_capa_seleccionada(posicion, capa_clicada, objeto_en_capa)
        else:
            self.gestor_seleccion.seleccion.objeto_seleccionado = None
        self.control_cambios.registrar(CodigoObjetoEspecial.seleccion)



    def _obtener_capa_clicada(self, posicion_en_pantalla: PosicionEnPantalla) -> Optional[CapaIndividual]:
        capa_clicada = None
        for capa in reversed(self.vista.areas.dibujo.capas.capa_dibujo.capas_internas):
            assert isinstance(capa, CapaIndividual)
            if self._es_capa_clicada(posicion_en_pantalla, capa):
                capa_clicada = capa
                break
        return capa_clicada

    def _es_capa_clicada(self, posicion_en_pantalla: PosicionEnPantalla, capa: CapaIndividual) -> bool:
        surface = capa.surface
        assert surface
        rect = surface.get_rect()
        posicion_relativa = obtener_posicion_relativa(posicion_en_pantalla, capa.posicion_capa)
        if not rect.collidepoint(posicion_relativa):
            return False
        if es_color_fondo(capa, posicion_relativa, surface):
            return False
        return True

    def seleccionar(self, capa: CapaIndividual) -> None:
        objeto_en_capa = self.vista.diccionario_objetos.get_item(capa.codigo)

        self.gestor_seleccion.seleccion.objeto_seleccionado = objeto_en_capa
        indice_capa_seleccionada = self.vista.areas.dibujo.capas.capa_dibujo.capas_internas.index(capa)
        self.gestor_seleccion.seleccion.indice_capa_seleccionada = indice_capa_seleccionada
        self.control_cambios.registrar(CodigoObjetoEspecial.seleccion)


    def borrar_capa_seleccionada(self) -> None:
        indice_capa_a_borrar = self.gestor_seleccion.seleccion.indice_capa_seleccionada
        if isinstance(indice_capa_a_borrar, int):
            self.gestor_seleccion.seleccion.indice_capa_seleccionada = None
            self.gestor_seleccion.seleccion.objeto_seleccionado = None
            self.vista.areas.dibujo.capas.capa_dibujo.capas_internas.pop(indice_capa_a_borrar)
            self.control_cambios.registrar(CodigoObjetoEspecial.dibujo)
            self.control_cambios.registrar(CodigoObjetoEspecial.seleccion)

    def modificar_circulo_seleccionado(self, direccion: str) -> None:
        if objeto_seleccionado := self.gestor_seleccion.seleccion.objeto_seleccionado:
            assert isinstance(objeto_seleccionado, Forma)
            assert objeto_seleccionado.tipo == 'circulo'
            self.gestor_seleccion_circulo.modificar_circulo(direccion)

    def salir(self) -> NoReturn:
        print(cadenas.FINALIZACION_USUARIO)
        raise SalirApp

    def cambiar_zoom(self, coeficiente: float) -> None:
        assert coeficiente > 0
        original = self.visualizacion.valor_zoom
        modificado = round(original * coeficiente, 2)
        if modificado == original:
            if coeficiente > 1:
                modificado += 0.01
        self.visualizacion.valor_zoom = modificado
        self.control_cambios.registrar(CodigoObjetoEspecial.visualizacion)
        print(f'Cambiando el zoom a {self.visualizacion.valor_zoom}')

    def _log_capa_seleccionada(self, posicion_en_pantalla: PosicionEnPantalla, capa_clicada: CapaIndividual, objeto_en_capa: ObjetoVectorial) -> None:
        posicion_en_documento = self.vista.visualizacion.pasar_a_documento(posicion_en_pantalla)
        log.anotar(f'Se ha seleccionado {capa_clicada} en {posicion_en_documento}', cat.seleccion)
        log.anotar(f'La forma que hay en esa capa es {objeto_en_capa}', cat.seleccion)

# Funciones independientes


def obtener_posicion_relativa(posicion: PosicionEnPantalla, posicion_base: PosicionEnPantalla) -> PosicionEnPantallaRelativa:
    return PosicionEnPantallaRelativa(convertir_a_tupla_dos_int(posicion.restar(posicion_base)))


def es_color_fondo(capa: CapaIndividual, posicion_relativa: PosicionEnPantallaRelativa, surface: GenericSurface) -> bool:
    assert surface.get_rect().collidepoint(posicion_relativa)
    color_en_posicion = surface.get_at(posicion_relativa)
    return color_en_posicion[:3] == capa.color_fondo
