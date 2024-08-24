from boa3.sc.compiletime import public
from boa3.sc.storage import get_read_only_context
from boa3.sc.storage.storagecontext import StorageContext


@public
def main() -> StorageContext:
    return get_read_only_context()
