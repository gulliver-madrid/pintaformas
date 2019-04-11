
from ...dependencias import PygameEvent
from .tipos import EventoParaJson, ListaTotalEventosParaJSON, ListaTotalDeEventos

class ConversorAEventosParaJSON:
    def convertir(self, lista_eventos: ListaTotalDeEventos) -> ListaTotalEventosParaJSON:
        """
        Convierte una lista de listas de eventos pygame en una lista de listas de eventos para json.
        """
        eventos_para_json = []
        for eventos_ciclo in lista_eventos:
            convertidos = [
                self.convertir_en_evento_para_json(evento)
                for evento in eventos_ciclo
            ]
            eventos_para_json.append(convertidos)
        return eventos_para_json

    def convertir_en_evento_para_json(self, evento: PygameEvent) -> EventoParaJson:
        return EventoParaJson(
            tipo=evento.type,
            dicc=evento.__dict__
        )
