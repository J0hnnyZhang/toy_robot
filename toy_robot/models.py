from abc import ABC, abstractmethod
from enum import Enum
from typing import List


class Facing(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def right(self) -> "Facing":
        return Facing((self.value + 1) % 4)

    def left(self) -> "Facing":
        return Facing((self.value + 3) % 4)


class Position:
    def __init__(self, x: int, y: int, f: Facing):
        self.x, self.y, self.f = x, y, f

    def front(self) -> "Position":
        x, y = self.x, self.y
        match self.f:
            case Facing.NORTH:
                y += 1
            case Facing.WEST:
                x -= 1
            case Facing.SOUTH:
                y -= 1
            case Facing.EAST:
                x += 1
            case _:
                raise ValueError(
                    f"This branch should not be touched, Facing value should be in {[f.name for f in Facing]}"
                )
        return Position(x, y, self.f)

    def change_facing(self, facing: Facing) -> None:
        self.f = facing

    def change_facing_to(self, facing: str):
        match facing.lower():
            case "left":
                facing_to = self.f.left()
            case "right":
                facing_to = self.f.right()
            case _:
                raise NotImplementedError(
                    "Invalid arguments, only 'left' and 'right' is allowed for now"
                )

        self.change_facing(facing_to)

    def __repr__(self) -> str:
        return f"{self.x},{self.y},{self.f.name}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y and self.f == other.f


class Table:
    def __init__(self, width: int = 5, length: int = 5):
        if width < 1 or length < 1:
            raise ValueError(
                "A table should not has negative or zero value for length or width"
            )
        self.max_x, self.max_y = width - 1, length - 1


class Navigator:
    def __init__(self, table: Table):
        self.table = table

    def safe(self, position: Position) -> bool:
        x, y = position.x, position.y
        return 0 <= x <= self.table.max_x and 0 <= y <= self.table.max_y


class RobotPrototype(ABC):
    @abstractmethod
    def set_position(self, position: Position):
        pass

    @abstractmethod
    def turn_left(self) -> None:
        pass

    @abstractmethod
    def turn_right(self) -> None:
        pass

    @abstractmethod
    def move_forward(self) -> None:
        pass

    @abstractmethod
    def report(self) -> None:
        pass

    @abstractmethod
    def await_orders(self, commands: List[str]):
        pass
