from typing import Any

from boa3.internal import constants
from boa3.internal.model.callable import Callable
from boa3.internal.model.method import Method
from boa3.internal.model.property import Property
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.classes.classarraytype import ClassArrayType
from boa3.internal.model.type.classes.classscope import ClassScope
from boa3.internal.model.type.classes.classtype import ClassType
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class UserClass(ClassArrayType):
    def __init__(self, identifier: str, decorators: list[Callable] = None,
                 bases: list[ClassType] = None):
        super(ClassArrayType, self).__init__(identifier, decorators, bases)

        self._static_methods: dict[str, Method] = {}

        self._class_variables: dict[str, Variable] = {}
        self._class_methods: dict[str, Method] = {}

        self._instance_variables: dict[str, Variable] = {}
        self._instance_methods: dict[str, Method] = {}
        self._properties: dict[str, Property] = {}

        self.imported_symbols = {}

    @property
    def shadowing_name(self) -> str:
        return 'class'

    @property
    def class_variables(self) -> dict[str, Variable]:
        class_vars = super().class_variables
        class_vars.update(self._class_variables)
        return class_vars

    @property
    def instance_variables(self) -> dict[str, Variable]:
        instance_vars = super().instance_variables
        instance_vars.update(self._instance_variables)
        return instance_vars

    @property
    def properties(self) -> dict[str, Property]:
        props = super().properties
        props.update(self._properties)
        return props

    @property
    def static_methods(self) -> dict[str, Method]:
        static_funcs = super().static_methods
        static_funcs.update(self._static_methods)
        return static_funcs

    @property
    def class_methods(self) -> dict[str, Method]:
        class_funcs = super().class_methods
        class_funcs.update(self._class_methods)
        return class_funcs

    @property
    def instance_methods(self) -> dict[str, Method]:
        instance_funcs = super().instance_methods
        instance_funcs.update(self._instance_methods)
        return instance_funcs

    def include_variable(self, var_id: str, var: Variable, is_instance: bool):
        """
        Includes a variable into the list of class variables

        :param var_id: variable identifier
        :param var: variable to be included
        :param is_instance: whether is a instance variable or a class variable
        """
        if not is_instance:
            self._class_variables[var_id] = var
        else:
            self._instance_variables[var_id] = var

    def include_property(self, prop_id: str, prop: Property):
        """
        Includes a property into the list of properties

        :param prop_id: property identifier
        :param prop: property to be included
        """
        self._properties[prop_id] = prop

    def include_callable(self, method_id: str, method: Callable, scope: ClassScope = ClassScope.INSTANCE) -> bool:
        """
        Includes a method into the scope of the class

        :param method_id: method identifier
        :param method: method to be included
        :param scope: which class scope this method should be included
        """
        from boa3.internal.model.builtin.builtin import Builtin
        if isinstance(method, Method):
            if Builtin.ClassMethodDecorator in method.decorators or scope is ClassScope.CLASS:
                methods_map = self._class_methods
            elif Builtin.StaticMethodDecorator in method.decorators or scope is ClassScope.STATIC:
                methods_map = self._static_methods
            else:
                methods_map = self._instance_methods

            if method_id not in methods_map:
                methods_map[method_id] = method
                return True

        return False

    def include_symbol(self, symbol_id: str, symbol: ISymbol, scope: ClassScope = ClassScope.INSTANCE):
        """
        Includes a method into the scope of the module

        :param symbol_id: method identifier
        :param symbol: method to be included
        :param scope: which class scope this symbol should be included
        """
        if symbol_id not in self.symbols:
            if isinstance(symbol, Variable):
                self.include_variable(symbol_id, symbol, scope == ClassScope.INSTANCE)
            elif isinstance(symbol, Property):
                self.include_property(symbol_id, symbol)
            elif isinstance(symbol, Callable):
                self.include_callable(symbol_id, symbol, scope)
            else:
                self.imported_symbols[symbol_id] = symbol

    def constructor_method(self) -> Method | None:
        if constants.INIT_METHOD_ID not in self._class_methods:
            from boa3.internal.model.type.classes.classinitmethoddefault import ClassInitMethod
            self._class_methods[constants.INIT_METHOD_ID] = ClassInitMethod(self)

        return self._class_methods[constants.INIT_METHOD_ID]

    def is_type_of(self, value: Any) -> bool:
        if value is self:
            return True
        return any(base.is_type_of(value) for base in self.bases)

    @classmethod
    def _is_type_of(cls, value: Any) -> bool:
        return isinstance(value, UserClass)

    @classmethod
    def build(cls, value: Any) -> IType:
        return cls()


_EMPTY_CLASS = UserClass('-internal_use')
