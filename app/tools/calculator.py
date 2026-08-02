from langchain_core.tools import tool


@tool
def calculator(x: float, y: float, op: str) -> float:
    """Perform operations (op) on x and y"""

    op = op.lower()

    if op in ["add", "+", "sum", "plus"]:
        return x + y

    if op in ["subtract", "-", "minus"]:
        return x - y

    if op in ["multiply", "*", "times", "product"]:
        return x * y

    if op in ["divide", "/", "quotient"]:
        if y == 0:
            raise ValueError("Division by zero is not allowed.")
        return x / y

    if op in ["power", "^", "**", "exponent"]:
        return x**y

    if op in ["modulus", "%", "mod"]:
        if y == 0:
            raise ValueError("Modulus by zero is not allowed.")
        return x % y

    if op in ["floor_divide", "//", "floordiv"]:
        if y == 0:
            raise ValueError("Division by zero is not allowed.")
        return x // y

    if op in ["root", "nth_root"]:
        if x < 0 and y % 2 == 0:
            raise ValueError("Even root of a negative number is not real.")
        return x ** (1 / y)

    raise ValueError(f"Unsupported operation: {op}")
