
from pathlib import Path

from .dependencias_log import AjustesLog, LogConTipos
from . import categorias, loggers


MARGEN = ' ' * 4
RUTA_LOGS_RELATIVA = "../../../logs"


class GestorLogPintaFormas:
    def ajustar_log(self, log: LogConTipos) -> None:
        ajustes_reparto: AjustesLog = AjustesLog(
            totales=categorias.totales,
            loggers=loggers.LOGGERS,
        )
        ruta_logs = self._get_ruta_logs()
        log.log_multinivel.set_config(ajustes_reparto, ruta_logs, MARGEN)

    def _get_ruta_logs(self) -> Path:
        ruta_absoluta = Path(__file__)
        assert ruta_absoluta.is_absolute()
        ruta_este_directorio = ruta_absoluta.parent

        ruta_logs = ruta_este_directorio / RUTA_LOGS_RELATIVA
        return ruta_logs.resolve()
