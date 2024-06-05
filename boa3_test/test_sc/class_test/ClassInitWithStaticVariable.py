from typing import Any

from boa3.sc.compiletime import public

FOO = "bar"


class MyNFT:
    def __init__(self, shape: str, color: str, background: str, size: str) -> None:
        self.shape = shape
        self.color = color
        self.background = background
        self.size = size

    def export(self) -> dict:
        return {
            'shape': self.shape,
            'color': self.color,
            'background': self.background,
            'size': self.size
        }


@public
def test() -> Any:
    nft = MyNFT('Rectangle', 'Blue', 'Black', 'Small')
    return nft
