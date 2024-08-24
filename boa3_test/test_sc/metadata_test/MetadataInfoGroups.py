from boa3.sc.compiletime import NeoMetadata, public


@public
def main() -> int:
    return 5


def permissions_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.add_group("033d523f36a732974c0f7dbdfafb5206ecd087211366a274190f05b86d357f4bad",
                   "QqtxfL5kHskQXtH5Jmg8+OoM6ltJF5gCpZlujpE9AvdZhzfns4I2jSZaxm+evA/nLRJpQlKmupXfuj2P8viQQg==")

    return meta
