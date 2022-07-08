from boa3.builtin import NeoMetadata, metadata, public


@public
def main() -> int:
    return 5


@metadata
def permissions_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.add_group("031f64da8a38e6c1e5423a72ddd6d4fc4a777abe537e5cb5aa0425685cda8e063b",
                   "gC+8ybKTjuQxBgPaFD/R+SrlZlERMK7aDe6+99XUulv/nD2Mco4pEbrESMa6Sc6WtjmSsRiI9ILf7LGRGQCmGA==")

    return meta
