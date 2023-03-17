class NotLoadedException(Exception):
    def __init__(self, empty_script: bool = False):
        self.empty_script = empty_script

    @property
    def message(self) -> str:
        exception_message = ''
        if self.empty_script:
            exception_message = 'An empty script was generated'

        return exception_message
