from typing import Dict

from boa3.model.builtin.interop.nativecontract import RoleManagementMethod
from boa3.model.variable import Variable


class GetDesignatedByRoleMethod(RoleManagementMethod):
    def __init__(self):
        from boa3.model.type.type import Type
        from boa3.model.builtin.interop.role.roletype import RoleType
        from boa3.model.type.collection.sequence.ecpointtype import ECPointType

        identifier = 'get_designated_by_role'
        native_identifier = 'getDesignatedByRole'

        role_type = RoleType.build()
        args: Dict[str, Variable] = {
            'role': Variable(role_type),
            'index': Variable(Type.int)
        }
        super().__init__(identifier, native_identifier, args, return_type=ECPointType.build())
