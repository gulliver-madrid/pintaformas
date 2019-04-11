from ...elementos.herramienta import Herramienta


SEP = ' ' * 3

TEXTO_ATAJOS_DE_TECLADO = f'''ATAJOS DE TECLADO:
1: Reducir Zoom{SEP}2: Aumentar Zoom{SEP}Ctrl-Z: Deshacer{SEP}Ctrl-Shift-Z: Rehacer'''

TEXTOS = {
    Herramienta.lapiz_libre: f'''Herramienta LÁPIZ
Usa los iconos de herramientas para cambiar de modo.
Haz click en un color de la derecha para seleccionarlo.
Para hacer un trazo, manten pulsado el raton mientras lo desplazas.
{TEXTO_ATAJOS_DE_TECLADO}
B: Borrar pantalla{SEP}R: Resetear (descartas el dibujo, no se puede deshacer)
''',
    Herramienta.circulo: f'''Herramienta CIRCULO
Crea un circulo relleno arrastrando el raton con el boton pulsado.
Antes de soltar el botón del ratón, puedes usar las flechas
para cambiar el COLOR (izqda-dcha) o el TAMAÑO (arriba-abajo)
Para volver al modo LÁPIZ, usa el icono.
{TEXTO_ATAJOS_DE_TECLADO}
''',
    Herramienta.recta: f'''Herramienta RECTA
Con esta herramienta puedes crear lineas rectas
{TEXTO_ATAJOS_DE_TECLADO}
''',
    Herramienta.seleccion: f'''Herramienta SELECCION
Con esta herramienta puedes seleccionar elementos
para transformarlos
{TEXTO_ATAJOS_DE_TECLADO}
''',
}
