from pathlib import Path
from types import NoneType  # type: ignore [attr-defined]
from typing import Optional, Sequence, Union

from ..compartido import es, es_instancia
from .categoria_actual import CategoriaActualLista
from .impresora import ImpresoraLog
from .contexto_log import ContextoLog
from .tipos import AjustesLog, LogMultinivelError, Logger, VariacionNivel


SILENCIO_TOTAL = False
CODIGO_CATEGORIA_ACTUAL = '<cat>'
ESPACIO = " "
MARGEN_POR_DEFECTO = ESPACIO * 2

ARCHIVO_REGISTRO_ERRORES = 'registro_errores.log'
NOMBRE_ARCHIVO_REGISTRO = "registro.log"



class LogMultinivel:
    __slots__ = ('margen', 'abrir_autocierre', 'log_activado', 'registro_errores', 'impresora', 'categoria_actual_lista', 'categorias_totales', 'loggers', 'debug_log')
    registro_errores: list[LogMultinivelError]
    margen: str
    categoria_actual_lista: CategoriaActualLista
    abrir_autocierre: ContextoLog
    log_activado: bool
    impresora: ImpresoraLog
    categorias_totales: Sequence[str]
    loggers: Sequence[Logger]
    debug_log: bool

    def __init__(self) -> None:
        self.margen = MARGEN_POR_DEFECTO
        self.abrir_autocierre = ContextoLog(self)
        self.registro_errores = []
        self.log_activado = False
        self.debug_log = False

    def set_config(self,
        ajustes_categorias: Optional[AjustesLog] = None,
        ruta_logs: Optional[Union[Path, str]] = None,
        margen: Optional[str] = None
    ) -> None:
        '''
        Establece la configuracion del log. Si no se incorporan argumentos, el log estara silenciado.

        Si hay argumentos, estos serviran para configurar las categorias, el silencio / visibilidad y las rutas
        '''
        if not ajustes_categorias:
            self.log_activado = False
            return
        if not ruta_logs:
            raise LogMultinivelError.ruta_logs_no_indicada()
        if isinstance(ruta_logs, str):
            ruta_logs = Path(ruta_logs)
        if not ruta_logs.exists():
            ruta_logs.mkdir()
            if not ruta_logs.exists():
                raise LogMultinivelError.ruta_logs_no_existe(ruta_logs)
        self.impresora = ImpresoraLog(ruta_logs)
        self.categoria_actual_lista = CategoriaActualLista()
        self.categorias_totales = es(ajustes_categorias.totales, list)
        self.loggers = es(ajustes_categorias.loggers, list)
        self.log_activado = True

        if margen:
            self.margen = margen


    def abrir(self, categoria: str, mensaje: str) -> None:
        if self.log_activado:
            self._anotar(mensaje, VariacionNivel.AUMENTAR, categoria)

    def cerrar(self, categoria: Optional[str] = None, mensaje: Optional[str] = None) -> None:
        if not mensaje:
            mensaje = ''
        if self.log_activado:
            self._anotar(mensaje, VariacionNivel.REDUCIR, categoria)

    def imprimir_logs(self) -> None:
        """Envia los logs pendientes de imprimir"""
        if not self.log_activado:
            raise LogMultinivelError('No pueden imprimirse logs: log no activado')
        texto_registro = self.categoria_actual_lista.get_texto_registro()
        if texto_registro:
            self.impresora.imprimir_en_archivo(texto_registro, NOMBRE_ARCHIVO_REGISTRO)

        self.impresora.imprimir_todo_en_archivos()
        if self.registro_errores:
            texto_errores = '\n'.join([error.msj for error in self.registro_errores])
        else:
            texto_errores = "No hubo errores en el proceso de logging"
        self.impresora.imprimir_en_archivo(texto_errores, ARCHIVO_REGISTRO_ERRORES)


    def anotar(self, mensaje: str, categoria: Optional[str] = None) -> None:
        self._anotar(mensaje, VariacionNivel.DEJAR_IGUAL, categoria)

    def _anotar(self, mensaje: str, modificador: VariacionNivel, categoria: Optional[str] = None) -> None:
        # print(f'+++++ {self.categoria_actual_lista.actual}')
        if not self.log_activado:
            return

        if self.debug_log:
            print(f'anotar: {mensaje}, modificador={modificador}, categoria={categoria}')

        if modificador is not None and not isinstance(modificador, VariacionNivel):
            raise LogMultinivelError.modificador_no_valido(modificador)

        if SILENCIO_TOTAL:
            return

        if modificador is VariacionNivel.REDUCIR:
            # print(f'Reduciendo categoria: {categoria}')
            self._reducir_nivel(categoria)


        if categoria:
            try:
                self._comprobar_validez_categoria(categoria)
            except LogMultinivelError as error:
                if not error.msj in (error.msj for error in self.registro_errores):
                    self.registro_errores.append(error)
                print(f"LogMultinivel: ignorando categoria {categoria}")
                return
            if CODIGO_CATEGORIA_ACTUAL in mensaje:
                mensaje = anadir_nombre_categoria(mensaje, categoria)

        for logger in self.loggers:
            if self._debe_imprimirse(categoria, logger):
                self._registrar_mensaje(mensaje, logger)

        if modificador is VariacionNivel.AUMENTAR:
            # print(f'Aumentando categoria: {categoria}')
            if not categoria:
                raise LogMultinivelError.falta_nombre_categoria_aumentar_nivel()
            self._aumentar_nivel(categoria)


        if self.nivel_actual < 0:
            raise LogMultinivelError.nivel_log_menor_que_cero(self.nivel_actual)


    def _debe_imprimirse(self, categoria: Optional[str], logger: Logger) -> bool:
        elementos_categoria = self.categoria_actual_lista.actual.copy()
        if categoria:
            elementos_categoria.append(categoria)
        categorias_visibles = logger.visibles
        categorias_imprimir_todo = logger.imprimir_todo
        assert es_instancia(categorias_visibles, (list, NoneType))  # type: ignore [arg-type]
        return (
            criterio_categorias_visibles(
                elementos_categoria, categorias_visibles
            ) or
            criterio_imprimir_todo(
                elementos_categoria, categorias_imprimir_todo
            )
        )



    def _comprobar_validez_categoria(self, categoria: str) -> None:
        '''Comprueba que la categoria especificada tiene un formato valido
        y se encuentra en la lista de totales'''
        assert ESPACIO not in categoria
        if self.categorias_totales == None:
            # No se comprueba pertenencia
            return

        if categoria not in self.categorias_totales:
            raise LogMultinivelError.categoria_no_conocida(categoria, self.categorias_totales)


    def _registrar_mensaje(self, mensaje: str, logger: Logger) -> None:
        """Se separan las lineas para no perder el margen en mensajes multilinea"""
        for linea in mensaje.split('\n'):
            self._imprimir_mensaje_con_margen(linea, logger)


    def _imprimir_mensaje_con_margen(self, mensaje: str, logger: Logger) -> None:
        margen = self.margen * self.nivel_actual
        self.impresora.registrar(margen + mensaje, logger)

    def _reducir_nivel(self, categoria: Optional[str]) -> None:
        if categoria:
            self._validar_cierre(categoria)
        self.categoria_actual_lista.quitar_actual()


    def _aumentar_nivel(self, categoria: str) -> None:
        self.categoria_actual_lista.anadir(categoria)

    @property
    def nivel_actual(self) -> int:
        return len(self.categoria_actual_lista.actual)

    def _validar_cierre(self, categoria: str) -> None:
        actual = self.categoria_actual_lista.actual[-1]
        if categoria != actual:
            raise LogMultinivelError.cierre_no_valido(categoria, actual)


def anadir_nombre_categoria(mensaje: str, categoria: str) -> str:
    """Atajo para anadir automaticamente el nombre de la categoria en el mensaje del log"""
    categoria_con_mayuscula_inicial = formatear_como_frase(categoria)
    return mensaje.replace(CODIGO_CATEGORIA_ACTUAL, categoria_con_mayuscula_inicial)


def formatear_como_frase(categoria: str) -> str:
    assert not ESPACIO in categoria
    con_espacios = categoria.replace('_', ' ')
    return inicia_con_mayuscula(con_espacios)


def inicia_con_mayuscula(cadena: str) -> str:
    return cadena[0].upper() + cadena[1:]


def criterio_categorias_visibles(elementos_categoria: Sequence[str], categorias_visibles: Optional[Sequence[str]]) -> bool:
    return all(
        elemento in categorias_visibles
        for elemento in elementos_categoria
    ) if categorias_visibles else False


def criterio_imprimir_todo(elementos_categoria: Sequence[str], categorias_imprimir_todo: Optional[Sequence[str]]) -> bool:
    return any(
        elemento in categorias_imprimir_todo
        for elemento in elementos_categoria
    ) if categorias_imprimir_todo else False
