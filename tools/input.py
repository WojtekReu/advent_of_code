def read_input(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def grid_one(data: str) -> list[str]:
    """
    Create grid where all lines have one string.
    """
    grid = [line for line in data.split("\n")]
    return grid


class BasePoint:
    def __init__(self, y, x, char):
        self.y = y
        self.x = x
        self.c = char

    def __repr__(self):
        return f"{self.c}{self.y}{self.x}"
