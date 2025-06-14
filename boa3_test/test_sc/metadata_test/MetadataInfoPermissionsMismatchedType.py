from boa3.sc.compiletime import NeoMetadata, public


@public
def Main() -> int:
    return 5


def permissions_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.add_permission(methods=[b'onNEP17Payment'])
    meta.add_permission(methods=[123])
    meta.add_permission(methods=[True])
    meta.add_permission(methods=b'onNEP17Payment')
    meta.add_permission(methods=123)
    meta.add_permission(methods=True)
    meta.add_permission(methods=(1, 2, 3))
    meta.add_permission(methods=(b'onNEP17Payment', 123, True))

    meta.add_permission(contract=b'12345678901234567890')
    meta.add_permission(contract=123)
    meta.add_permission(contract=True)
    meta.add_permission(contract=['0x3846a4aa420d9831044396dd3a56011514cd10e3'])

    meta.add_permission(contract=123, methods=b'onNEP17Payment')

    return meta
