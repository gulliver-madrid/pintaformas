from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, Optional
from ..vista.visualizacion import Visualizacion
from ..tipos import PosicionEnPantalla
from ..elementos.formas import Linea
from .dibujador_en_documento import DibujadorEnDocumento
from .gestor_seleccion import GestorSeleccion

if TYPE_CHECKING:
    from .realizador import Realizador


@dataclass
class TrazoIniciado:
    origen: PosicionEnPantalla


class Lapiz:
    visualizacion: Final[Visualizacion]
    dibujador_en_documento: Final[DibujadorEnDocumento]
    gestor_seleccion: Final[GestorSeleccion]
    trazo_iniciado: Optional[TrazoIniciado]

    def __init__(self,
        visualizacion: Visualizacion,
        dibujador_en_documento: DibujadorEnDocumento,
        gestor_seleccion: GestorSeleccion
    ):
        self.visualizacion = visualizacion
        self.dibujador_en_documento = dibujador_en_documento
        self.gestor_seleccion = gestor_seleccion
        self.trazo_iniciado = None

    def realizar_trazo(self, origen_en_pantalla: PosicionEnPantalla, destino_en_pantalla: PosicionEnPantalla) -> None:
        origen = self.visualizacion.pasar_a_documento(origen_en_pantalla)
        destino = self.visualizacion.pasar_a_documento(destino_en_pantalla)
        self.gestor_seleccion.selecciona_linea(origen, destino)
        linea = self.gestor_seleccion.seleccion.objeto_seleccionado
        assert isinstance(linea, Linea), linea
        self.dibujador_en_documento.dibuja_linea(linea)
        self.gestor_seleccion.deseleccionar()

    def iniciar_trazo(self, posicion: PosicionEnPantalla) -> None:
        self.trazo_iniciado = TrazoIniciado(posicion)

    def finalizar_trazo(self, posicion: PosicionEnPantalla) -> None:
        assert self.trazo_iniciado
        self.realizar_trazo(self.trazo_iniciado.origen, posicion)
        self.trazo_iniciado = None


    def mantener_trazo_recto(self, posicion: PosicionEnPantalla) -> None:
        '''Mantiene una linea recta aun no finalizada'''
        # Esto habra que sustituirlo
        assert self.trazo_iniciado
        origen_pantalla = self.trazo_iniciado.origen
        destino_pantalla = posicion
        origen = self.visualizacion.pasar_a_documento(origen_pantalla)
        destino = self.visualizacion.pasar_a_documento(destino_pantalla)
        seleccion = self.gestor_seleccion.seleccion
        if (objeto_seleccionado := seleccion.objeto_seleccionado) and isinstance(objeto_seleccionado, Linea):
            seleccion.objeto_seleccionado = None
        self.gestor_seleccion.selecciona_linea_imaginaria(origen, destino)
