
from typing import Final

from ...dependencias import PygameEvent
from ...log_pintaformas import cat, log
from ..control_general.dibujador_en_documento import DibujadorEnDocumento
from ..gestor_eventos.gestor_eventos import GestorDeEventos
from ..persistencia.sistema_persistencia import DocumentoBase
from ..persistencia.transformar_datos.formatos_documento import Documento
from ..vista.vista import Vista
from .doc_en_memoria import DocumentoEnMemoria
from .medidor_tiempo import MedidorTiempo, SituacionMedidorTiempo


class AppGeneral:
    __slots__ = (
        'titulo',
        'vista',
        'documento_en_memoria',
        'dibujador_en_documento',
        'gestor_eventos',
        '_medidor_tiempo',
    )
    _medidor_tiempo: Final[MedidorTiempo]
    titulo: str
    vista: Vista
    documento_en_memoria: DocumentoEnMemoria
    dibujador_en_documento: DibujadorEnDocumento
    gestor_eventos: GestorDeEventos

    def __init__(self,
            titulo: str,
            vista: Vista,
            documento_en_memoria: DocumentoEnMemoria,
            dibujador_en_documento: DibujadorEnDocumento,
            gestor_eventos: GestorDeEventos,
            medidor_tiempo: MedidorTiempo):
        self.titulo = titulo
        self.vista = vista
        self.documento_en_memoria = documento_en_memoria
        self.dibujador_en_documento = dibujador_en_documento
        self.gestor_eventos = gestor_eventos
        self._medidor_tiempo = medidor_tiempo


    def iniciar(self) -> None:
        self.vista.crear_areas_principales()
        self.vista.iniciar_renderizador()
        self.gestor_eventos.realizador.establece_valores_iniciales()
        self.vista.actualizar_cambios()


    def cargar_documento_en_espacio_de_trabajo(self, documento: Documento, nombre_documento: str) -> None:
        categoria_log = cat.persistencia.cargando_documento_en_espacio_de_trabajo
        msj_log = f"\n<cat>: {nombre_documento}"
        with log.log_multinivel.abrir_autocierre(
            categoria_log, msj_log, end="Hecho"
        ):
            formas_recuperadas = documento.capas
            for forma in formas_recuperadas:
                self.dibujador_en_documento.dibuja_forma(forma)
        nuevo_titulo = f'{self.titulo} Documento: {nombre_documento}'
        self.vista.poner_titulo(nuevo_titulo)


    def ejecutar_ciclo(self, eventos: list[PygameEvent]) -> None:
        log.anotar(f"Incorporando {len(eventos)} eventos")
        self.gestor_eventos.incorporar_eventos(eventos)
        self.gestor_eventos.procesar_eventos()
        log.anotar('Todos los eventos fueron procesados')
        self._actualizar_vista()

    def _actualizar_vista(self) -> None:
        self._medidor_tiempo.registrar(SituacionMedidorTiempo.INICIO_ACTUALIZACION_VISTA)
        self.vista.actualizar_cambios()
        self._medidor_tiempo.registrar(SituacionMedidorTiempo.FIN_ACTUALIZACION_VISTA)

    def get_documento_base(self) -> DocumentoBase:
        return (self.documento_en_memoria, self.dibujador_en_documento.capas)
