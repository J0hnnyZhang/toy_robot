from abc import ABC, abstractmethod

from toy_robot.models import Facing, Position, RobotPrototype


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class PlaceCommand(Command):
    def __init__(self, robot: RobotPrototype, x: int, y: int, f: Facing):
        self.robot = robot
        self.position = Position(x, y, f)

    def execute(self) -> None:
        self.robot.set_position(self.position)


class MoveCommand(Command):
    def __init__(self, robot: RobotPrototype):
        self.robot = robot

    def execute(self):
        self.robot.move_forward()


class LeftCommand(Command):
    def __init__(self, robot: RobotPrototype):
        self.robot = robot

    def execute(self) -> None:
        self.robot.turn_left()


class RightCommand(Command):
    def __init__(self, robot: RobotPrototype):
        self.robot = robot

    def execute(self) -> None:
        self.robot.turn_right()


class ReportCommand(Command):
    def __init__(self, robot: RobotPrototype):
        self.robot = robot

    def execute(self) -> None:
        self.robot.report()
