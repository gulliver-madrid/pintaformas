
from ..core.general.app import AppGeneral
from .programa import Programa


class ProgramaConPersistencia(Programa[AppGeneral]):

    def _procedimientos_iniciales_extra(self) -> None:
        if (self.persistencia and self.ajustes['cargar_dibujo_guardado']):
            # Carga en la app el dibujo guardado
            documento, nombre = self.persistencia.cargar_dibujo_guardado_en_espacio_de_trabajo()
            self.app.cargar_documento_en_espacio_de_trabajo(documento, nombre)

    def _procedimientos_finales_extra(self) -> None:
        """Guarda el dibujo si esta activada la persistencia"""
        if self.persistencia and self.ajustes['grabar_dibujo_al_salir']:
            documento_base = self.app.get_documento_base()
            self.persistencia.guardar_dibujo(documento_base)
