from ..log_pintaformas import log
from ..core.ajustes_generales import AjustesGenerales


class AnalizadorLineaComandos:
    @staticmethod
    def obtener_ajustes_usuario(argumentos: list[str]) -> AjustesGenerales:
        '''
        Recibe los argumentos de linea de comandos, devuelve los ajustes_usuario
        Estos pueden ser:
            --new
            --load <nombre>
            --fps <numero>
            -np, --no_persistencia
            -gev (grabar eventos)
            -lev, --load-events (cargar eventos)
        '''
        ajustes_usuario = AjustesGenerales()
        indices_a_ignorar: list[int] = []

        if '--load' not in argumentos:
            argumentos.append('--new')
        for i, arg in enumerate(argumentos):

            if i in indices_a_ignorar:
                continue

            if arg == '--new':
                ajustes_usuario['cargar_dibujo_guardado'] = False

            elif arg == '--fps':
                if argumentos[i + 1].isdigit():
                    fps = int(argumentos[i + 1])
                    indices_a_ignorar.append(i + 1)
                else:
                    raise Exception("El parametro siguiente a --fps debe ser un numero")
                ajustes_usuario['fps'] = fps

            elif arg == '--load':
                if "--new" in argumentos:
                    class ArgumentosIncompatibles(Exception):
                        pass
                    raise ArgumentosIncompatibles()
                if len(argumentos) == (i + 1) or argumentos[i + 1].startswith('-'):
                    raise Exception("Falta un nombre de archivo despues de --load")
                nombre_archivo = argumentos[i + 1]
                assert '.' not in nombre_archivo  # pq por ahora debe ser un directorio
                ajustes_usuario['nombre_documento_proporcionado_por_el_usuario'] = nombre_archivo
                indices_a_ignorar.append(i + 1)

            elif arg in ('--no_persistencia', '-np'):
                ajustes_usuario['usar_persistencia'] = False
                ajustes_usuario['cargar_dibujo_guardado'] = False
                ajustes_usuario['grabar_dibujo_al_salir'] = False

            elif arg in ('--debug-log', '-dl'):
                log.log_multinivel.debug_log = True
                print('Modo DEBUG activado')


            elif arg in ('--load-events', '-lev'):
                if len(argumentos) == (i + 1) or argumentos[i + 1].startswith('-'):
                    raise Exception("Falta el nombre de los eventos a cargar")
                eventos_a_cargar = argumentos[i + 1]
                ajustes_usuario['eventos_a_cargar'] = eventos_a_cargar
                assert '.' not in eventos_a_cargar
                indices_a_ignorar.append(i + 1)

            elif arg in ('--grabar-eventos', '-gev'):
                ajustes_usuario['grabar_eventos'] = True

            else:
                raise Exception(f"Argumento desconocido: {arg}")

        return ajustes_usuario
