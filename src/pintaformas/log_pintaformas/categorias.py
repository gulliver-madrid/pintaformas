from .dependencias_log import Categoria, GrupoCategorias, obtener_categorias_totales


Cat = Categoria

class CategoriaPersistencia(GrupoCategorias):
    cargando_documento_en_espacio_de_trabajo = Cat('cargando_documento_en_espacio_de_trabajo')
    guardar_documento = Cat('guardar_documento')
    guardar_documento_en_archivo = Cat('guardar_documento_en_archivo')


class CategoriaGestionDeEventos(GrupoCategorias):
    evento_en_gev_normal = Cat('evento_en_gev_normal')
    evento_en_gev_seleccion_circulo = Cat('evento_en_gev_seleccion_circulo')
    procesar_eventos = Cat('procesar_eventos')
    procesar_evento = Cat('procesar_evento')
    todos_los_eventos = Cat('todos_los_eventos')


class cat(GrupoCategorias):
    eventos = CategoriaGestionDeEventos
    persistencia = CategoriaPersistencia
    control_cambios = Cat('control_cambios')
    crear_marca = Cat('crear_marca')
    movimiento_cursor = Cat('movimiento_cursor')
    programa = Cat('programa')
    preparacion_general = Cat('preparacion_general')
    info_ciclo = Cat('info_ciclo')
    mostrar_tiempo = Cat('mostrar_tiempo')
    renderizador = Cat('renderizador')
    cambio_herramienta = Cat('cambio_herramienta')
    operador_grafico = Cat('operador_grafico')
    cursor = Cat('cursor')
    seleccion = Cat('seleccion')
    vista = Cat('vista')
    tests = Cat('tests')


CATEGORIAS_PERSISTENCIA = [
    cat.persistencia.cargando_documento_en_espacio_de_trabajo,
    cat.persistencia.guardar_documento,
    cat.persistencia.guardar_documento_en_archivo,
]
CATEGORIAS_EVENTOS = [
    cat.eventos.procesar_evento,
    cat.eventos.evento_en_gev_normal,
    cat.eventos.evento_en_gev_seleccion_circulo,
]
CATEGORIAS_IMPRESCINDIBLES = [
    cat.crear_marca,
    cat.programa,
]


totales = obtener_categorias_totales(cat)
