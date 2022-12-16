from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage import get_read_only_context
from boa3.builtin.interop.storage.storagecontext import StorageContext


@public
def main() -> StorageContext:
    return get_read_only_context()
