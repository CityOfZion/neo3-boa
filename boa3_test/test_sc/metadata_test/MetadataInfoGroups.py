from boa3.builtin.compile_time import NeoMetadata, public


@public
def main() -> int:
    return 5


def permissions_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.add_group("031f64da8a38e6c1e5423a72ddd6d4fc4a777abe537e5cb5aa0425685cda8e063b",
                   "fhsOJNF3N5Pm3oV1b7wYTx0QVelYNu7whwXMi8GsNGFKUnu3ZG8z7oWLfzzEz9pbnzwQe8WFCALEiZhLD1jG/w==")

    return meta
