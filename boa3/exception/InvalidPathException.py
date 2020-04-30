class InvalidPathException(Exception):
    def __init__(self, path: str):
        self.__path = path

    def __str__(self) -> str:
        return 'Invalid path: %s' % self.__path
