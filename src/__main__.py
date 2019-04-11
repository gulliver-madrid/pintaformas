from .pintaformas.inicio.inicio import Inicio

inicio: Inicio

def main() -> None:
    global inicio
    inicio = Inicio()
    inicio.activar()

if __name__ == '__main__':
    main()
