"""
Commands for the robot
"""
from abc import ABC, abstractmethod

from toy_robot.models import Facing, Position, RobotPrototype


class Command(ABC):
    """
    Command base class, define the command interface
    """

    def __init__(self, robot: RobotPrototype):
        self.robot = robot

    @abstractmethod
    def execute(self) -> None:
        """
        command execute
        :return: No return value
        """


class PlaceCommand(Command):
    """
    PLACE command, used to set the position of the robot on the table
    """

    def __init__(self, robot: RobotPrototype, x: int, y: int, facing: Facing):
        super().__init__(robot)
        self.position = Position(x, y, facing)

    def execute(self) -> None:
        self.robot.set_position(self.position)


class MoveCommand(Command):
    """
    MOVE command, used to move the robot 1 step forward
    """

    def execute(self):
        self.robot.move_forward()


class LeftCommand(Command):
    """
    LEFT command, used to turn the robot left
    """

    def execute(self) -> None:
        self.robot.turn_left()


class RightCommand(Command):
    """
    RIGHT command, used to turn the robot right
    """

    def execute(self) -> None:
        self.robot.turn_right()


class ReportCommand(Command):
    """
    REPORT command, used to order the robot to report it's current position on the table
    """

    def execute(self) -> None:
        self.robot.report()
