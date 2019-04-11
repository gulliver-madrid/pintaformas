import time

def obtener_fecha_actual() -> str:
    segundos = time.time()
    local_time = time.ctime(segundos)
    return local_time
