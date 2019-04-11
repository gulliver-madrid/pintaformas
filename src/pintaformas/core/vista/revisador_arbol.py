from ...log_pintaformas import log, cat
from ..general.control_cambios import ControlDeCambios
from ..tipos.cev import CodigoObjetoEspecial, CodigoStr, codigo_to_string
from .capas import Capa, CapaContenedora
from .objeto_capas_internas import ObjetoConCapasInternas


class RevisadorArbol:
    def __init__(self, control_cambios: ControlDeCambios) -> None:
        self.control_cambios = control_cambios

    def revisar_arbol(self, contenedora: ObjetoConCapasInternas) -> list[CodigoStr]:
        """
        Revisa el contenido de un objeto con capas internas y devuelve un listado de lo que hay que renderizar.
        """
        renderizar_todo = (CodigoObjetoEspecial.visualizacion in self.control_cambios)
        return self._revisar_arbol(contenedora, renderizar_todo)


    def _revisar_arbol(self, contenedora: ObjetoConCapasInternas, renderizar_todo: bool) -> list[CodigoStr]:
        """
        Metodo interno que revisa el contenido de un objeto con capas internas y devuelve un listado de lo que hay que renderizar.
        """
        codigos_a_renderizar = []
        log.anotar(f'Revisando contenedora {contenedora.codigo}', cat.renderizador)
        for capa in contenedora.capas_internas:
            codigos_a_renderizar_en_hija = self._revisar_capa(capa, renderizar_todo)
            codigos_a_renderizar.extend(codigos_a_renderizar_en_hija)

        if codigos_a_renderizar:
            codigo_a_anadir = codigo_to_string(contenedora.codigo)
            log.anotar(f"Añadiendo contenedora: {codigo_a_anadir}", cat.renderizador)
            codigos_a_renderizar.append(codigo_a_anadir)
        return codigos_a_renderizar

    def _revisar_capa(self, capa: Capa, renderizar_todo: bool) -> list[CodigoStr]:
        log.anotar(f'Revisando {capa.codigo}', cat.renderizador)
        if hasattr(capa, 'capas_internas'):
            assert isinstance(capa, CapaContenedora)
            if codigos_a_renderizar := self._revisar_arbol(capa, renderizar_todo):
                assert codigo_to_string(capa.codigo) in codigos_a_renderizar
                return codigos_a_renderizar

        # Podemos no tener capas internas, o tenerlas pero no tener que renderizarlas
        # Y aun asi, tener que renderizar esta capa
        if (capa.codigo in self.control_cambios) or renderizar_todo:
            codigo_a_anadir = codigo_to_string(capa.codigo)
            log.anotar(f"Añadiendo capa: {codigo_a_anadir}", categoria=cat.renderizador)
            return [codigo_a_anadir]
        return []
