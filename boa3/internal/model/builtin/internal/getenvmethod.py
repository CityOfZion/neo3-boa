from typing import Any

from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.method import IBuiltinMethod


class GetEnvMethod(IBuiltinMethod):
    def __init__(self, env: str = None):
        from boa3.internal import constants
        from boa3.internal.model.type.type import Type

        identifier = '-get_env'
        super().__init__(identifier, return_type=Type.str)
        self._env = env if isinstance(env, str) and len(env) > 0 else constants.DEFAULT_CONTRACT_ENVIRONMENT

    @property
    def _args_on_stack(self) -> int:
        return super()._args_on_stack

    def generate_opcodes(self, code_generator):
        code_generator.convert_literal(self._env)

    @property
    def _body(self) -> str | None:
        return None

    def update_with_analyser(self, analyser):
        from boa3.internal.analyser.analyser import Analyser
        if isinstance(analyser, Analyser):
            self.reset()
            self._env = analyser.env

        super().update_with_analyser(analyser)

    def build(self, value: Any = None) -> IBuiltinMethod:
        if isinstance(value, str):
            result = GetEnvMethod(value)
        else:
            result = super().build(value)
        return result


class EnvProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'env'
        getter = GetEnvMethod()
        super().__init__(identifier, getter)
        self._getter: GetEnvMethod = self._getter  # ensure typing

    def build(self, env: str = None, *args, **kwargs) -> IBuiltinProperty:
        getter = self._getter.build(env)
        if getter != self._getter:
            result = EnvProperty()
            result._getter = getter
        else:
            result = super().build(env, *args, **kwargs)
        return result


Env = EnvProperty()
