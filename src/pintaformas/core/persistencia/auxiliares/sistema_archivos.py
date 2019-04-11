from pathlib import Path
from ...excepciones import DirectorioYaExiste


class InterfazSistemaArchivos:
    '''Funciona como interfaz para operar con el sistema de archivos'''

    def listar_directorio(self, ruta_directorio: Path) -> list[str]:
        return [ruta.name for ruta in ruta_directorio.iterdir()]

    def crear_directorio(self, ruta_directorio: Path) -> None:
        if self.es_directorio(ruta_directorio):
            raise DirectorioYaExiste(ruta_directorio)
        ruta_directorio.mkdir()

    def es_directorio(self, ruta_directorio: Path) -> bool:
        assert ruta_directorio.exists()
        return ruta_directorio.is_dir()

    def existe_ruta(self, ruta: Path) -> bool:
        return ruta.exists()
