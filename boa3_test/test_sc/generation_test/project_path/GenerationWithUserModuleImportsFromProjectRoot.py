# only compile if pass boa3_test/test_sc/generation_test as project root
from GenerationWithUserModuleImports import with_param

from boa3.sc.compiletime import public
from boa3.sc.types import UInt160, Notification


@public
def main(args: list, key: UInt160) -> list[Notification]:
    return with_param(args, key)
