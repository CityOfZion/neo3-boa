from boa3.internal.model.variable import Variable


class FunctionArguments:

    def __init__(self):
        self._args: dict[str, Variable] = {}
        self._vararg: tuple[str, Variable] | None = None
        self._kwargs: dict[str, Variable] | None = None

    @property
    def args(self) -> dict[str, Variable]:
        return self._args.copy()

    def add_arg(self, arg_id: str, arg: Variable) -> bool:
        if not isinstance(arg, Variable):
            return False
        self._args[arg_id] = arg
        return True

    @property
    def vararg(self) -> tuple[str, Variable] | None:
        return self._vararg

    def set_vararg(self, arg_id: str, arg: Variable) -> bool:
        if not isinstance(arg, Variable):
            return False
        self._vararg = (arg_id, arg)
        return True

    @property
    def kwargs(self) -> dict[str, Variable]:
        return self._kwargs

    def add_kwarg(self, arg_id: str, arg: Variable) -> bool:
        if not isinstance(arg, Variable):
            return False
        if self._kwargs is None:
            self._kwargs: dict[str, Variable] = {}
        self._kwargs[arg_id] = arg
        return True
