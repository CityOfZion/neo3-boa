from boa3.builtin.compile_time import NeoMetadata, metadata, public


@public
def main() -> int:
    return 5


@metadata
def permissions_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.add_group("031f64da8a38e6c1e5423a72ddd6d4fc4a777abe537e5cb5aa0425685cda8e063b",
                   "DPr9wBXZO0kDZjZNhTnXh+kZyHcX7V1xW5HA1n37hhn//2BtC9tlajCaykZJQZoj+VQdlQ3gHNw5bx9iSXe2mA==")

    return meta
