from __future__ import annotations

from typing import Any, Dict, Optional, Set


class ScopeValue:
    def __init__(self):
        self._values: Dict[str, Any] = {}
        self._assigned_variables: Set[str] = set()
        self._parent_scope: Optional[ScopeValue] = None

    def new_scope(self) -> ScopeValue:
        scope = ScopeValue()
        scope._values = self._values.copy()
        scope._assigned_variables = self._assigned_variables.copy()
        scope._parent_scope = self
        return scope

    def previous_scope(self) -> Optional[ScopeValue]:
        return self._parent_scope

    def update_values(self, *scopes, is_loop_scope: bool = False):
        other_scopes = [scope for scope in scopes if isinstance(scope, ScopeValue) and scope._parent_scope == self]
        if len(other_scopes) == 0:
            return

        first_scope = other_scopes[0]
        common_keys: Set[str] = set(first_scope._values)
        common_assigns: Set[str] = first_scope._assigned_variables

        for scope in other_scopes[1:]:
            common_keys = common_keys.intersection(set(scope._values))
            common_assigns = common_assigns.intersection(scope._assigned_variables)

        new_values = {}
        different_values = []

        for key in common_keys:
            values = []
            for scope in other_scopes:
                if scope[key] not in values:
                    values.append(scope[key])

            if len(values) == 1:
                new_values[key] = values.pop()
            else:
                different_values.append(key)

        # if there are variables assigned with the same value in all scopes, include this value to the outer scope
        if not is_loop_scope:
            self._values = new_values
        else:
            self._values = {key: value for key, value in new_values.items()
                            if key in self._values and self._values[key] == value}
        self._assigned_variables = self._assigned_variables.union(common_assigns)

        # if there are different value depending on the scope, there's no way to guarantee the value in the actual
        # scope anymore, so remove it from the dictionary
        for key in different_values:
            if key in self._values:
                self._values.pop(key)

    def reset(self):
        self._values.clear()
        self._assigned_variables.clear()

    def assign(self, key: str):
        self._assigned_variables.add(key)

    def remove(self, key: str):
        if key in self._values:
            self._values.pop(key)

    def __contains__(self, item: str) -> bool:
        return item in self._values

    def __getitem__(self, key: str) -> Any:
        if key in self._values:
            return self._values[key]
        else:
            return None

    def __setitem__(self, key: str, value: Any):
        self._values[key] = value


class UndefinedType:
    def __init__(self):
        pass

    @property
    def identifier(self) -> str:
        return 'undefined'


Undefined = UndefinedType()
