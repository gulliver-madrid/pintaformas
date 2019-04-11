from pathlib import Path


class ExcepcionPintaFormas(BaseException):
    pass

class ExcepcionLeve(ExcepcionPintaFormas):
    '''Refleja un ligero contratiempo que el problema puede gestionar
    y seguir funcionando'''
    pass

class NoTieneNumero(ExcepcionLeve):
    '''
    Lo lanza una funcion que busca un numero dentro de un nombre
    si no hay ningun numero.
    '''
    pass

class ErrorDeRuta(ExcepcionLeve):
    def __init__(self, ruta: Path) -> None:
        self.ruta = ruta
    def __str__(self) -> str:
        return f'\n\nruta: {self.ruta}'

class ErrorEnProcesoDeCarga(ErrorDeRuta):
    pass



class DirectorioYaExiste(ErrorDeRuta):
    pass



class NoHayArchivosConEsaRaizAcabadosEnNumero(ExcepcionLeve):
    def __init__(self, raiz: str):
        self.raiz = raiz
    def __str__(self) -> str:
        return f'\n\nNo se encontro ningun archivo que empezase por {self.raiz} y acabase en un numero'


class NoHayArchivosConEsaRaiz(NoHayArchivosConEsaRaizAcabadosEnNumero):
    pass

class SalirApp(Exception):
    def __str__(self) -> str:
        return "\n\nEl usuario decidio salir de la app"
