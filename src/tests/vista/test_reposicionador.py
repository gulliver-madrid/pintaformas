import unittest
import pygame
from dataclasses import dataclass

from ...pintaformas.dependencias import nombres_pygame, PygameSurface
from ...pintaformas.core.tipos import Dimensiones, Posicion, PosicionEnPantalla, Tuple2Int
from ...pintaformas.core.vista.renderizador.reposicionador import Reposicionador
from ...pintaformas.libs.compartido import es_instancia


@dataclass
class DatoLinea:
    origen: Posicion
    destino: Posicion
    grosor: int


LADO_SURFACE_CONTENEDOR = 200
MOSTRAR_GRAFICAMENTE = 0

DIMENSIONES_CONTENEDOR = Dimensiones((LADO_SURFACE_CONTENEDOR, LADO_SURFACE_CONTENEDOR))
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
TRANSPARENTE = (1, 1, 1)

KEYS_SETS_DATOS = ('descripcion', 'lineas')


@dataclass
class Datos:
    descripcion: str
    lineas: list[DatoLinea]


def crear_dato_linea(origen: Tuple2Int, destino: Tuple2Int, grosor: int) -> DatoLinea:
    return DatoLinea(Posicion((20, 20)), Posicion((30, 30)), 3)


SETS_DATOS = [
    Datos(
        descripcion='linea_descendente',
        lineas=[crear_dato_linea((20, 20), (30, 30), 3)]
    ),
    Datos(
        descripcion='linea_ascendente',
        lineas=[crear_dato_linea((40, 40), (60, 20), 5)]
    ),
    Datos(
        descripcion='linea_ascendente_fina',
        lineas=[crear_dato_linea((30, 30), (40, 20), 1)]
    ),
    Datos(
        descripcion='linea_ascendente_muy_gruesa',
        lineas=[crear_dato_linea((40, 40), (50, 30), 12)]
    ),
    Datos(
        descripcion='linea_descendente_inversa',
        lineas=[crear_dato_linea((30, 30), (20, 20), 3)]
    ),
    Datos(
        descripcion='linea_ascendente_inversa',
        lineas=[crear_dato_linea((30, 20), (20, 30), 5)]
    ),
    Datos(
        descripcion='dos_lineas_con_diferente_grosor',
        lineas=[
            crear_dato_linea((30, 20), (20, 30), 5),
            crear_dato_linea((20, 30), (30, 30), 12),
        ]
    ),
]


class TestReposicionador(unittest.TestCase):


    def test_pintar_linea_sin_usar_reposicionador(self) -> None:
        '''Testea usando una capa grande'''
        for set_datos in SETS_DATOS:
            _descripcion = set_datos.descripcion
            lineas = set_datos.lineas
            contenedor1 = self.crear_surface_con_linea((DIMENSIONES_CONTENEDOR), lineas[0])
            for linea in lineas:
                pygame.draw.line(contenedor1, BLANCO, linea.origen, linea.destino, linea.grosor)
            contenedor2 = PygameSurface(DIMENSIONES_CONTENEDOR)
            for linea in lineas:
                capa = self.crear_surface_con_linea(DIMENSIONES_CONTENEDOR, linea, transparente=True)
                contenedor2.blit(capa, (0, 0))
            self.check_equivalencia_surfaces(contenedor1, contenedor2)



    def test_pintar_linea_usando_reposicionador(self) -> None:
        '''Testea pintar la linea en una capa pequena y luego ubicarla en la
        capa grande'''
        for set_datos in SETS_DATOS:
            descripcion = set_datos.descripcion
            lineas = set_datos.lineas
            with self.subTest(descripcion=descripcion, lineas=lineas):
                self.check_pintar_lineas_usando_reposicionador(lineas)




    def check_pintar_lineas_usando_reposicionador(self, lineas: list[DatoLinea]) -> None:
        '''Realiza el test para una linea en concreto'''
        reposicionador = Reposicionador()
        # surface de control
        contenedor1 = self.crear_surface_con_linea(DIMENSIONES_CONTENEDOR, lineas[0])
        for linea in lineas[1:]:
            pygame.draw.line(contenedor1, BLANCO, linea.origen, linea.destino, linea.grosor)

        largos_lineas = [reposicionador.calcular_largo_linea(linea.origen, linea.destino) for linea in lineas]

        # surface usando capa pequena
        contenedor2 = PygameSurface(DIMENSIONES_CONTENEDOR)
        lineas_internas = []
        for linea in lineas:
            origen = PosicionEnPantalla(linea.origen)
            destino = PosicionEnPantalla(linea.destino)
            posicion_capa, dimensiones_capa, origen_interno, destino_interno = \
                reposicionador.hallar_posicion_y_dimensiones_capa(origen, destino, linea.grosor, Dimensiones(DIMENSIONES_CONTENEDOR))
            linea_interna = DatoLinea(origen_interno, destino_interno, linea.grosor)
            lineas_internas.append(linea_interna)
            capa = self.crear_surface_con_linea(dimensiones_capa, linea_interna, transparente=True)
            contenedor2.blit(capa, posicion_capa)
        if MOSTRAR_GRAFICAMENTE:
            presentador = PresentadorGraficoSurfaces()
            presentador.mostrar_graficamente(contenedor1, contenedor2)
        largos_lineas_internas = [reposicionador.calcular_largo_linea(linea.origen, linea.destino) for linea in lineas_internas]
        self.assertEqual(largos_lineas, largos_lineas_internas, f'Las lineas deberian tener la misma longitud')
        self.check_equivalencia_surfaces(contenedor1, contenedor2)


    def check_equivalencia_surfaces(self, surface1: PygameSurface, surface2: PygameSurface) -> None:
        fallos = self.comparar_contenedores(surface1, surface2)
        for descripcion_fallo, fallos_concretos in fallos.items():
            self.assertEqual([], fallos_concretos, f'{descripcion_fallo}')

    def crear_surface_con_linea(self, dimensiones: Dimensiones, linea: DatoLinea, transparente: bool = False) -> PygameSurface:
        surface = PygameSurface(dimensiones)
        if transparente:
            surface.set_colorkey(TRANSPARENTE)
            surface.fill(TRANSPARENTE)
        pygame.draw.line(surface, BLANCO, linea.origen, linea.destino, linea.grosor)
        return surface

    def comparar_contenedores(self, contenedor1: PygameSurface, contenedor2: PygameSurface) -> dict[str, list[Tuple2Int]]:
        fallos: dict[str, list[Tuple2Int]] = dict(
            se_esperaba_blanco=[],
            se_esperaba_negro=[]
        )

        for x in range(LADO_SURFACE_CONTENEDOR):
            for y in range(LADO_SURFACE_CONTENEDOR):
                pixel_1 = contenedor1.get_at((x, y))
                pixel_2 = contenedor2.get_at((x, y))
                if pixel_1 != pixel_2:
                    pixel_2_as_tuple = pixel_2[:3]
                    assert es_instancia(pixel_2_as_tuple, tuple)
                    if pixel_2[:3] == NEGRO:
                        fallos['se_esperaba_blanco'].append((x, y))
                    elif pixel_2[:3] == BLANCO:
                        fallos['se_esperaba_negro'].append((x, y))
                    else:
                        raise RuntimeError(f'{pixel_1} != {pixel_2}')
        return fallos


class PresentadorGraficoSurfaces:
    def mostrar_graficamente(self, *surfaces: PygameSurface) -> None:
        DIMENSIONES = (600, 600)
        pygame.init()
        for i, surface in enumerate(surfaces):
            num_caso = i + 1
            ventana = pygame.display.set_mode(DIMENSIONES)
            self._mostrar(ventana, surface, f'caso {num_caso}')
            seguir = True
            while seguir:
                for evento in pygame.event.get():
                    if evento.type == nombres_pygame.QUIT:
                        seguir = False

    @staticmethod
    def _mostrar(ventana: PygameSurface, surface: PygameSurface, nombre_caso: str) -> None:
        ventana.blit(surface, (0, 0))
        pygame.display.set_caption(nombre_caso)
        pygame.display.update()



if __name__ == '__main__':
    unittest.main()
