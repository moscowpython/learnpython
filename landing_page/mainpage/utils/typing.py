from typing import Optional, TypeVar

_T = TypeVar("_T")


def ensured(value: Optional[_T]) -> _T:
    assert value
    return value
