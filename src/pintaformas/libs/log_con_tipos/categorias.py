from typing import NewType, Type


Categoria = NewType('Categoria', str)

Categorias = list[Categoria]


class GrupoCategorias:

    def __init__(self) -> None:
        raise RuntimeError("La clase Categoria y sus derivadas no pueden instanciarse")


def obtener_categorias_totales(grupo_principal:Type[GrupoCategorias]) -> list[Categoria] :
    totales: list[Categoria] = []
    clases_a_revisar: list[Type[GrupoCategorias]] = [grupo_principal]
    for clase in clases_a_revisar:
        valor: object
        for atributo, valor in clase.__dict__.items():
            if atributo.startswith('__'):
                continue
            if isinstance(valor, str):
                assert atributo == valor, f"Discrepancia entre nombre del atributo ({atributo}) y valor ({valor})"
                totales.append(Categoria(valor))
                continue
            assert isinstance(valor, type)
            assert issubclass(valor, GrupoCategorias)
            clases_a_revisar.append(valor)
    return totales
