from abc import ABC, abstractmethod

from toy_robot.models import Facing, Position, RobotPrototype


class Command(ABC):
    def __init__(self, robot: RobotPrototype):
        self.robot = robot

    @abstractmethod
    def execute(self) -> None:
        pass


class PlaceCommand(Command):
    def __init__(self, robot: RobotPrototype, x: int, y: int, facing: Facing):
        super().__init__(robot)
        self.position = Position(x, y, facing)

    def execute(self) -> None:
        self.robot.set_position(self.position)


class MoveCommand(Command):
    def execute(self):
        self.robot.move_forward()


class LeftCommand(Command):
    def execute(self) -> None:
        self.robot.turn_left()


class RightCommand(Command):
    def execute(self) -> None:
        self.robot.turn_right()


class ReportCommand(Command):
    def execute(self) -> None:
        self.robot.report()
