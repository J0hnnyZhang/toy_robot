"""
Data models or robot basic class
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List


class Facing(Enum):
    """
    The facing directions
    """

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def right(self) -> "Facing":
        """
        Calculate the right direction
        :return: a new Facing direction
        """
        return Facing((self.value + 1) % 4)

    def left(self) -> "Facing":
        """
        Calculate the left direction
        :return: a new Facing direction
        """
        return Facing((self.value + 3) % 4)


class Position:
    """
    The value of x, y and facing direction of the robot on the table
    """

    def __init__(self, x: int, y: int, facing: Facing):
        self.x, self.y, self.facing = x, y, facing

    def front(self) -> "Position":
        """
        Calculate the front position
        :return: a new Position
        """
        x, y = self.x, self.y
        match self.facing:
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
        return Position(x, y, self.facing)

    def change_facing(self, facing: Facing) -> None:
        """
        set the facing
        :param facing: facing direction to set
        :return: no return value
        """
        self.facing = facing

    def change_facing_to(self, relative_facing: str) -> None:
        """
        change facing to a new facing direction
        :param relative_facing: a relative facing direction upon Position.facing, should be either 'left' or 'right'
        :return: no return value
        """
        match relative_facing.lower():
            case "left":
                facing_to = self.facing.left()
            case "right":
                facing_to = self.facing.right()
            case _:
                raise NotImplementedError(
                    "Invalid arguments, only 'left' and 'right' is allowed for now"
                )

        self.change_facing(facing_to)

    def __repr__(self) -> str:
        return f"{self.x},{self.y},{self.facing.name}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y and self.facing == other.facing


@dataclass
class Table:
    """
    Data model of table, which the robot will play on
    """

    max_x: int
    max_y: int

    def __init__(self, width: int = 5, length: int = 5):
        if width < 1 or length < 1:
            raise ValueError(
                "A table should not has negative or zero value for length or width"
            )
        self.max_x, self.max_y = width - 1, length - 1


class Navigator:
    """
    Navigator for the robot, help robot detect safe and unsafe movements
    """

    def __init__(self, table: Table):
        self.table = table

    def safe(self, position: Position) -> bool:
        """
        Check whether the position to move is safe or not
        :param position: position to move
        :return: True for safe, False for unsafe
        """
        x, y = position.x, position.y
        return 0 <= x <= self.table.max_x and 0 <= y <= self.table.max_y


class RobotPrototype(ABC):
    """
    Robot base class, robot interface, define what a robot can do
    """

    @abstractmethod
    def set_position(self, position: Position) -> None:
        """
        Where to put the robot on the table
        :param position: position to set
        :return: no return value
        """

    @abstractmethod
    def turn_left(self) -> None:
        """
        Change the robot facing to left
        :return: no return value
        """

    @abstractmethod
    def turn_right(self) -> None:
        """
        Change the robot facing to right
        :return: no return value
        """

    @abstractmethod
    def move_forward(self) -> None:
        """
        Move the robot 1 step forward
        :return: no return value
        """

    @abstractmethod
    def report(self) -> None:
        """
        Report the current position of the robot
        :return: no return value
        """

    @abstractmethod
    def await_orders(self, commands: List[str]):
        """
        Robot is ready for the commands
        :param commands: commands to let the robot execute
        :return: no return value
        """
