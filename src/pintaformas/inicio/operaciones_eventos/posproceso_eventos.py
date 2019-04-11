import json
from pathlib import Path

from ...core.excepciones import NoHayArchivosConEsaRaiz, NoHayArchivosConEsaRaizAcabadosEnNumero

from ...log_pintaformas import log, cat
from ...core.persistencia.auxiliares.analizador_num_doc import AnalizadorNumerosArchivo
from .crear_texto_eventos import crear_texto_eventos
from .conversor_a_eventos_para_json import ConversorAEventosParaJSON
from .rutas import RUTA_EVENTOS_RELATIVA
from .tipos import ListaTotalEventosParaJSON, ListaTotalDeEventos


INDENTADO_JSON_GUARDADO_EVENTOS = 2


def get_directorio_guardado_eventos() -> Path:
    ruta_absoluta = Path(__file__)
    assert ruta_absoluta.is_absolute()
    ruta_este_directorio = ruta_absoluta.parent
    ruta_grabado_sin_normalizar = ruta_este_directorio / RUTA_EVENTOS_RELATIVA
    return ruta_grabado_sin_normalizar.resolve()



class PostprocesadorEventos:
    def __init__(self, eventos_guardados: ListaTotalDeEventos):
        self.eventos_guardados = eventos_guardados
        self.directorio_grabado = get_directorio_guardado_eventos()
        if not self.directorio_grabado.exists():
            self.directorio_grabado.mkdir()
        assert self.directorio_grabado.exists(), self.directorio_grabado

    def log_todos_los_eventos(self, ciclos_totales: int) -> None:
        eventos_guardados = self.eventos_guardados
        assert len(eventos_guardados) == ciclos_totales, \
            f'{len(eventos_guardados)} es diferente a {ciclos_totales}'
        # input('Pulsa ENTER para ver la lista de eventos\n')
        texto = crear_texto_eventos(eventos_guardados)
        num_eventos_totales = sum(len(eventos_ciclo) for eventos_ciclo in eventos_guardados)
        log.anotar(texto, cat.eventos.todos_los_eventos)
        print(f'\nTotal ciclos: {ciclos_totales}. Total eventos: {num_eventos_totales}')

    def grabar_eventos_en_disco(self) -> None:
        eventos_para_json = self.convertir_formato_eventos()
        self.grabar_eventos(eventos_para_json)


    def convertir_formato_eventos(self) -> ListaTotalEventosParaJSON:
        conversor = ConversorAEventosParaJSON()
        return conversor.convertir(self.eventos_guardados)


    def grabar_eventos(self, eventos_para_json: ListaTotalEventosParaJSON) -> None:
        cadena_json = json.dumps(eventos_para_json, indent=INDENTADO_JSON_GUARDADO_EVENTOS)
        analizador = AnalizadorNumerosArchivo()
        try:
            n = analizador.obtener_mayor_numero_documento(
                'eventos',
                list(path.name for path in self.directorio_grabado.iterdir())
            )
        except (NoHayArchivosConEsaRaiz, NoHayArchivosConEsaRaizAcabadosEnNumero):
                n = 1
        ruta_grabado = self.directorio_grabado / f'eventos{n+1}.json'
        with open(ruta_grabado, 'w') as archivo:
            archivo.write(cadena_json)
        print('Eventos guardados')
