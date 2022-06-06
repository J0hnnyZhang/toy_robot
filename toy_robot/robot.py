"""
Robot class for the toy robot game
"""
from typing import Optional, List

from toy_robot.command_interpreter import CommandsInterpreter
from toy_robot.commands import Command
from toy_robot.models import Position, Navigator, RobotPrototype


def _ensure_place_command_first(func):
    def wrapper(robot, *args):
        if not robot.current_position:
            raise ValueError(
                "Please use PLACE command to put the robot on the table first, then you can order the robot to move"
            )
        func(robot, *args)

    return wrapper


class Robot(RobotPrototype):
    """
    A concrete robot
    """

    def __init__(self, navigator: Navigator, position: Optional[Position] = None):
        self.current_position: Optional[Position] = None
        self.navigator: Navigator = navigator
        self.command_interpreter = CommandsInterpreter(self)

        if position:
            self.set_position(position)

    def set_position(self, position: Position) -> None:
        if self.navigator.safe(position):
            self.current_position = position
        else:
            x, y = self.navigator.table.max_x, self.navigator.table.max_y
            raise ValueError(
                f"Please put the robot on the table, in case of damaging it. The table max x and y is {x}, {y}"
            )

    @_ensure_place_command_first
    def turn_left(self) -> None:
        assert self.current_position is not None
        self.current_position.change_facing_to("left")

    @_ensure_place_command_first
    def turn_right(self) -> None:
        assert self.current_position is not None
        self.current_position.change_facing_to("right")

    @_ensure_place_command_first
    def move_forward(self) -> None:
        assert self.current_position is not None
        position = self.current_position.front()
        if self.navigator.safe(position):
            self.current_position = position
        else:
            print("This movement may endanger the robot, refuse to move")

    @_ensure_place_command_first
    def report(self) -> None:
        print(f"Output: {self.current_position}")

    def await_orders(self, commands: List[str]):
        cmds: List[Command] = self.command_interpreter.interpret(commands)
        for cmd in cmds:
            cmd.execute()
