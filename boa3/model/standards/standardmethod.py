from typing import Dict

from boa3.model.method import Method
from boa3.model.type.itype import IType
from boa3.model.type.type import Type
from boa3.model.variable import Variable


class StandardMethod(Method):
    def __init__(self, display_name: str,
                 args: Dict[str, IType] = None,
                 return_type: IType = Type.none,
                 safe: bool = False):
        if not isinstance(args, dict):
            args = {}
        method_args = {key: Variable(value) for key, value in args.items()}
        super().__init__(args=method_args, return_type=return_type, is_public=True,
                         external_name=display_name, is_safe=safe)
