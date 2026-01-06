from boa3.internal.model.builtin.interop.nativecontract import RoleManagementMethod
from boa3.internal.model.variable import Variable


class DesignateAsRoleMethod(RoleManagementMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.builtin.interop.role.roletype import RoleType
        from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType

        identifier = 'designate_as_role'
        native_identifier = 'designateAsRole'

        role_type = RoleType.build()
        args: dict[str, Variable] = {
            'role': Variable(role_type),
            'nodes': Variable(Type.list.build_collection([ECPointType.build()]))
        }
        super().__init__(identifier, native_identifier, args, return_type=Type.none)
