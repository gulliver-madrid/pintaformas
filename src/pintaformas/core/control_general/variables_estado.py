class VariableDeEstado:
    '''Solo el realizador puede modificarlas'''
    def __init__(self) -> None:
        self._valor: object = None

    @property
    def valor(self) -> object:
        return self._valor

    def set_valor(self, valor: object) -> None:
        self._valor = valor
