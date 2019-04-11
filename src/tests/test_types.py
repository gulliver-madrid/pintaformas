import importlib
from pathlib import Path
from types import ModuleType
from typing import Sequence
import unittest
import inspect

from ..meta import PROJECT_NAME, SRC_PROJECT
from .fixtures.types import DetalleClaseConFallos, obtener_fallos


EXCLUDE_PARTS = ('test', 'tests')
RelativeDir = str
DirTuple = tuple[Path, RelativeDir]


def get_all_modules(initial_path: Path, pkg: str) -> list[ModuleType]:
    initial = (initial_path, '.')
    dir_tuples: list[DirTuple] = [initial]
    modules: list[ModuleType] = []
    for directory, rel_dir in dir_tuples:
        paths = list(directory.iterdir())

        for path in paths:
            if path.is_dir():
                if any(excluded_part in path.parts for excluded_part in EXCLUDE_PARTS):
                    continue
                dir_tuples.append((path, rel_dir + path.name + "."))
            elif path.name.endswith(".py"):
                module_name = path.name[:-3]
                module = importlib.import_module(rel_dir + module_name, pkg)
                modules.append(module)
    return modules





class TestTypes(unittest.TestCase):

    def test_slots_implies_annotations(self) -> None:
        src_rel = "../../"
        this_file = Path(__file__)
        src = (this_file / src_rel).resolve()
        # print(src)
        modules = get_all_modules(src, SRC_PROJECT)
        clases = get_clases_propias(modules, PROJECT_NAME)
        # print(modules)
        # print(f"Encontradas {len(clases)} clases propias")
        # print(", ".join(sorted(clase.__name__ for clase in clases)))
        fallos, contador_fallos = obtener_fallos(list(clases))
        assert contador_fallos == sum(len(detalle.slots_sin_anotacion) for detalle in fallos)

        mensaje_fallo = crear_mensaje_fallo(fallos, contador_fallos)
        self.assertTrue(contador_fallos == 0, msg='\n\n' + mensaje_fallo)



def crear_mensaje_fallo(fallos: list[DetalleClaseConFallos], contador_fallos: int) -> str:
    err_msg_lines: list[str] = []
    if fallos:
        err_msg_lines.append("En las siguientes clases, existen atributos definidos en __slots__ que no tienen una anotacion de tipo:\n")
    for detalle in fallos:
        clase = detalle.clase
        nombre_clase_con_modulo = get_nombre_clase_con_modulo(clase, SRC_PROJECT)
        err_msg_lines.append(f"  {nombre_clase_con_modulo}")
        for slot in detalle.slots_sin_anotacion:
            err_msg_lines.append(f"    {slot}")
    err_msg_lines.append(f"\nEn total, hay {contador_fallos} atributos sin anotacion de tipo pese a estar definidos en __slots__")
    return '\n'.join(err_msg_lines)


def get_nombre_clase_con_modulo(clase: type, src_project: str) -> str:
    _, modulo = clase.__module__.split(src_project + '.')
    nombre_clase_con_modulo = f"{clase.__name__} ({modulo})"
    return nombre_clase_con_modulo




def get_clases_propias(modules: Sequence[ModuleType], project_name: str) -> set[type]:
    """
    Devuelve todas las clases definidas en la secuencia de modulos aportada
    """
    clases_propias = set()

    for module in modules:
        # print(f'\nClases encontradas en el modulo {module.__name__}:')
        names = dir(module)
        for name in names:
            obj = getattr(module, name)
            if type(obj) == type:
                try:
                    propia = project_name in inspect.getfile(obj)
                except TypeError:  # built-in classes
                    propia = False
                if propia:
                    # print(obj.__name__)
                    clases_propias.add(obj)
    return clases_propias


if __name__ == '__main__':
    unittest.main()


# https://stackoverflow.com/questions/63416336/import-module-from-different-directory-with-import-module
