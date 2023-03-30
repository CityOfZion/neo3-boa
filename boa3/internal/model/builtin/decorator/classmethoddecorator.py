import ast
from typing import Optional

from boa3.internal.model import set_internal_call
from boa3.internal.model.builtin.decorator.builtindecorator import IBuiltinDecorator
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.annotation import metatype
from boa3.internal.model.type.classes.userclass import UserClass


class ClassMethodDecorator(IBuiltinDecorator):
    def __init__(self):
        identifier = 'classmethod'
        super().__init__(identifier)

    def update_args(self, args: ast.arguments, origin: Optional[ISymbol] = None):
        if isinstance(origin, UserClass) and len(args.args) > 0 and args.args[0].annotation is None:
            # the user doesn't need to explicitly write the type of the first argument if it's a classmethod
            # the first argument is a Type[Class]
            cls_type = metatype.metaType.build(origin)
            cls_type_annotation = (cls_type.meta_identifier
                                   if isinstance(cls_type, metatype.MetaType)
                                   else cls_type.identifier)

            cls_ast_annotation = ast.parse(cls_type_annotation).body[0].value
            cls_ast_annotation = set_internal_call(cls_ast_annotation)
            args.args[0].annotation = cls_ast_annotation

    @property
    def has_cls_or_self(self) -> bool:
        return True
