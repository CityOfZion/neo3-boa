from typing import Any

from boa3.sc.compiletime import public


class Example:
    def __init__(self, shape: str, color: str, background: str, size: str):
        self.shape = shape
        self.color = color
        self.background = background
        self.size = size

    def test_value(self) -> dict[str, str]:
        return {
          'shape': self.shape,
          'color': self.color,
          'background': self.background,
          'size': self.size
        }

    def test_keys(self) -> dict[str, str]:
        return {
          self.shape: 'shape',
          self.color: 'color',
          self.background: 'background',
          self.size: 'size'
        }

    def test_pair(self) -> dict[str, str]:
        return {
          self.shape: self.shape,
          self.color: self.color,
          self.background: self.background,
          self.size: self.size
        }


@public
def test_only_values() -> Any:
    example = Example('Rectangle', 'Blue', 'Black', 'Small')
    return example.test_value()


@public
def test_only_keys() -> Any:
    example = Example('Rectangle', 'Blue', 'Black', 'Small')
    return example.test_keys()


@public
def test_pair() -> Any:
    example = Example('Rectangle', 'Blue', 'Black', 'Small')
    return example.test_pair()
