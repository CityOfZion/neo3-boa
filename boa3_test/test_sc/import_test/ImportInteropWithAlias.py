from boa3.builtin import interop as functions, public


@public
def Main():
    functions.runtime.notify('something')
