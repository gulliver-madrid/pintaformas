class Objeto:
    __slots__ = ()

    def __repr__(self) -> str:
        return self.ver()

    def ver(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name} ...{self._last_digits_id()}'

    def _last_digits_id(self) -> str:
        return str(id(self))[-3:]
