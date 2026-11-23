"""Live LSP acceptance fixture. Hover `greet` at the call near the bottom."""
from typing import overload


def greet(name: str, repeat: int = 1) -> str:
    """Build a greeting / 生成问候语。

    ## Parameters
    - `name`: the person to greet. 支持中文和 Unicode。
    - `repeat`: number of repetitions, defaults to `1`.

    ## Returns
    The greeting as a string.

    ## Example
    ```python
    greet("Islands", repeat=2)
    ```

    > Documentation, links and actions come from the language server.

    See [Python documentation](https://docs.python.org/3/library/stdtypes.html).
    """
    return " ".join([f"Hello, {name}!"] * repeat)


@overload
def identity(value: int) -> int: ...
@overload
def identity(value: str) -> str: ...
def identity(value: int | str) -> int | str:
    """Return the input. Use signature help to inspect both overloads."""
    return value


message = greet("Islands", repeat=2)
broken = greet(123)  # Intentional diagnostic for hover/copy/related actions.
result = identity("sample")
