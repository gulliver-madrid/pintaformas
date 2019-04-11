from ...pintaformas.dependencias import nombres_pygame, PygameEvent


ListaEventos = list[PygameEvent]


def generar_evento_salir() -> PygameEvent:
    evento_salir = PygameEvent(nombres_pygame.QUIT)
    return evento_salir


def obtener_listas_eventos_n_vacias_mas_salir(n: int) -> list[ListaEventos]:
    n_vacias = n
    evento_salir = generar_evento_salir()
    listas_eventos: list[ListaEventos] = [[] for i in range(n_vacias)]
    listas_eventos.append([evento_salir])
    return listas_eventos


def obtener_listas_eventos_dibujar_circulo() -> list[ListaEventos]:
    pulsar_c = PygameEvent(nombres_pygame.KEYDOWN, {'unicode': 'c', 'key': 99, 'mod': 0, 'scancode': 46, 'window': None})

    evento_salir = generar_evento_salir()
    listas_eventos = [[pulsar_c], [pulsar_c], [pulsar_c, pulsar_c], [evento_salir]]
    return listas_eventos
