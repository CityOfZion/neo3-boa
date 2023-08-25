from typing import Any


def decorator_method(func: Any):
    a = 123
    return func


@decorator_method
def main() -> Any:
    return []
