from boa3.builtin.compile_time import public
from boa3.sc.storage import get_context
from boa3.sc.storage.storagecontext import StorageContext


@public
def main() -> StorageContext:
    return get_context()
