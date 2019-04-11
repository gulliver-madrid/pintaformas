DEBUG = True

def info(*args: str) -> None:
    if DEBUG:
        print(*args)
