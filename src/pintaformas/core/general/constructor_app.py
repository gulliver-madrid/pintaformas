from typing import TYPE_CHECKING

from ..control_general.control_general import ControlGeneral
from ..control_general.dibujador_en_documento import DibujadorEnDocumento
from ..control_general.estado_herramienta import EstadoHerramienta
from ..control_general.gestor_cursor import GestorCursor
from ..control_general.gestor_seleccion import GestorSeleccion
from ..control_general.gestor_seleccion_circulo import GestorSeleccionCirculo
from ..control_general.realizador import Realizador
from ..elementos.cursor import Cursor
from ..elementos.seleccion import Seleccion
from ..gestor_eventos import crear_gestor_eventos
from ..vista.crear_vista import crear_vista
from ..vista.surfaces import PygameSurfaceWrapperFactory
from ..vista.vista import Vista
from .app import AppGeneral
from .control_cambios import ControlDeCambios
from .control_capas import ControlDeCapas
from .doc_en_memoria import DocumentoEnMemoria
from .medidor_tiempo import MedidorTiempo
from .observador_herramienta import EstadoHerramientaObservado

if TYPE_CHECKING:
    from ..elementos.forma import Forma
    from ..elementos.objeto_modelo import ObjetosModelo


class ConstructorAppGeneral:
    def __init__(self) -> None:
        self.surface_factory = PygameSurfaceWrapperFactory()

        self.medidor_tiempo = MedidorTiempo()


    def crear_app(self, titulo: str) -> AppGeneral:

        control_cambios = ControlDeCambios()
        control_capas = ControlDeCapas(control_cambios)
        cursor = Cursor()
        seleccion = Seleccion()
        objetos_modelo: ObjetosModelo = dict(
            cursor=cursor,
            seleccion=seleccion,
        )
        vista = crear_vista(self.surface_factory, objetos_modelo, control_capas)
        documento_en_memoria = DocumentoEnMemoria()
        dibujador_en_documento = crear_dibujador_en_documento(documento_en_memoria,  vista)
        gestor_cursor = GestorCursor(cursor)
        gestor_seleccion = GestorSeleccion(seleccion, vista, control_cambios)
        gestor_seleccion_circulo = GestorSeleccionCirculo(seleccion, vista, control_cambios)

        control_general = ControlGeneral(
            gestor_cursor=gestor_cursor,
            gestor_seleccion=gestor_seleccion,
            gestor_seleccion_circulo=gestor_seleccion_circulo,
            dibujador_en_documento=dibujador_en_documento,
            vista=vista
        )

        estado_herramienta = EstadoHerramienta()
        estado_herramienta_observado = EstadoHerramientaObservado(estado_herramienta)
        realizador = Realizador(control_general, control_cambios, estado_herramienta)
        gestor_eventos = crear_gestor_eventos(realizador, estado_herramienta_observado)

        return AppGeneral(titulo, vista, documento_en_memoria, dibujador_en_documento, gestor_eventos, self.medidor_tiempo)


def crear_dibujador_en_documento(documento_en_memoria: DocumentoEnMemoria, vista: Vista) -> DibujadorEnDocumento:
    capas: list[Forma] = []
    return DibujadorEnDocumento(documento_en_memoria, capas, vista)
