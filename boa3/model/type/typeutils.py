from typing import Any, Dict

from boa3.model.callable import Callable
from boa3.model.type.annotation.metatype import metaType
from boa3.model.type.typingmethod.casttypemethod import CastTypeMethod


class TypeUtils:
    @classmethod
    def all_functions(cls) -> Dict[str, Callable]:
        from boa3.model.builtin.builtincallable import IBuiltinCallable
        return {tpe._identifier: tpe for tpe in vars(cls).values() if isinstance(tpe, IBuiltinCallable)}

    # type for internal validation
    type = metaType

    # Annotation function utils
    cast = CastTypeMethod()
