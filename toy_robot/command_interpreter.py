from abc import ABC, abstractmethod
from typing import List, Optional

from toy_robot.commands import (
    MoveCommand,
    LeftCommand,
    RightCommand,
    ReportCommand,
    PlaceCommand,
    Command,
)
from toy_robot.models import Facing, RobotPrototype


class CommandTranslator(ABC):
    @staticmethod
    @abstractmethod
    def translate(robot: RobotPrototype, *command_text: str):
        pass


class CommandError(Exception):
    pass


class SimpleCommandsTranslator(CommandTranslator):
    @staticmethod
    def translate(robot: RobotPrototype, *command_text: str):
        if len(command_text) != 1:
            raise CommandError("Simple commands should not have args")
        cmd = command_text[0].upper()
        match cmd:
            case "MOVE":
                return MoveCommand(robot)
            case "LEFT":
                return LeftCommand(robot)
            case "RIGHT":
                return RightCommand(robot)
            case "REPORT":
                return ReportCommand(robot)
            case _:
                raise CommandError(
                    f"Unsupported command of {cmd}, supported simple commands: move, left, right, report"
                )


class ArgumentCommandsTranslator(CommandTranslator):
    @staticmethod
    def translate(robot: RobotPrototype, *command_text: str):
        if len(command_text) != 2:
            raise CommandError(
                "Argument commands must have args and args string should be the second argument, "
                "and multiple arguments should be separated by ','"
                "such as 'PLACE 0,0,NORTH'"
            )

        cmd = command_text[0].upper()
        args = command_text[1].split(",")

        match cmd:
            case "PLACE":
                return ArgumentCommandsTranslator._translate_place_command(robot, *args)
            case _:
                raise CommandError(
                    f"Unsupported command of {cmd}, supported argument commands: PLACE, such as 'PLACE 0,0,NORTH'"
                )

    @staticmethod
    def _translate_place_command(robot: RobotPrototype, *args):
        if len(args) != 3:
            raise CommandError(
                "PLACE command should has 3 args, represent 'x,y,FACING', such as '0,0,NORTH'"
            )
        x, y, f = args[0], args[1], args[2]

        try:
            return PlaceCommand(robot, int(x), int(y), Facing[f.upper()])
        except ValueError:
            raise CommandError("PLACE command x and y arguments must be integers")
        except KeyError:
            raise CommandError(
                f"PLACE command facing argument must be in {[f.name for f in Facing]}"
            )


class CommandsInterpreter:
    def __init__(self, robot: Optional[RobotPrototype]):
        self.robot = None
        if robot:
            self.init(robot)

    def init(self, robot: RobotPrototype):
        self.robot = robot

    def interpret(self, command_list: List[str]) -> List[Command]:
        if not self.robot:
            raise ValueError("Should call init before interpret")

        commands: List[Command] = []
        for command_text in command_list:
            cmd = command_text.split(" ")
            if len(cmd) > 1:
                commands.append(ArgumentCommandsTranslator.translate(self.robot, *cmd))
            else:
                commands.append(SimpleCommandsTranslator.translate(self.robot, *cmd))
        return commands
