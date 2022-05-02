class Example:
    def __init__(self, id_: int, arg1: str):
        self._var_int = id_
        self.var_str = arg1

    def export(self) -> dict:
        return {
            'text': self.var_str
        }
