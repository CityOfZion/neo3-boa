from boa3.sc import runtime
from boa3.sc.compiletime import public


@public
def hello_world() -> str:
    runtime.notify('Hello World!')
    return 'Test'
