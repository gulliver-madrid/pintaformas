from pathlib import Path

from .pintaformas.log_pintaformas import log
from .pintaformas.dependencias import appdirs

RUTA_MEDIOS_RELATIVA = '../media'

DATA_DIR_PARENT = "pintaformas-pygame"
DATA_DIR_CHILD = "data"


def get_data_dir() -> Path:
    data_dir = appdirs.user_data_dir(DATA_DIR_CHILD, DATA_DIR_PARENT, roaming=True)
    assert isinstance(data_dir, str)
    log.anotar(f"{data_dir=}")
    return Path(data_dir)


class Rutas:
    ruta_medios: Path
    directorio_documentos: Path

    def crear_rutas(self) -> None:
        ruta_absoluta = Path(__file__)
        assert ruta_absoluta.is_absolute()
        ruta_directorio_proyecto = Path(ruta_absoluta).parent

        ruta_medios = ruta_directorio_proyecto / RUTA_MEDIOS_RELATIVA
        self.ruta_medios=ruta_medios.resolve()

        if not self.ruta_medios.exists():
            print(f"Atención: la ruta en la que deberían hallarse los archivos estáticos ({self.ruta_medios}) no está disponible")
        directorio_documentos = get_data_dir()

        if not directorio_documentos.exists():
            directorio_documentos.mkdir(parents=True)
        self.directorio_documentos = directorio_documentos


rutas = Rutas()
rutas.crear_rutas()
