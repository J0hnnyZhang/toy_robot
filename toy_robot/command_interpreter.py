"""
Command interpreter which translate string commands into the commands which the robot can understand
"""
from abc import ABC, abstractmethod
from types import new_class
from typing import List, cast, Optional, Dict, Type

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
    """
    Command translator base class, define the command translator interface
    """

    command: str

    @classmethod
    @abstractmethod
    def translate(cls, robot: RobotPrototype, *args) -> Command:
        """
        Do translate a string typed command into a robot understandable command
        :param robot: which robot the command is upon
        :param args: arguments for the command
        :return: a Command object
        """


class CommandError(Exception):
    """
    Used for representing the errors while interpreting string typed commands into robot understandable commands
    """


SIMPLE_COMMANDS: Dict[str, Type[Command]] = {
    "MOVE": MoveCommand,
    "LEFT": LeftCommand,
    "RIGHT": RightCommand,
    "REPORT": ReportCommand,
}


def translate(cls, robot: RobotPrototype, *args) -> Command:
    """
    translate method for built command translator class
    :param cls: the class for a specific command translator
    :param robot: which robot the command is upon
    :param args: arguments for the command
    :return: a Command object
    """
    cmd = cls.command
    if cmd not in SIMPLE_COMMANDS:
        raise CommandError(
            f"Unsupported command of {cmd}, supported simple commands: move, left, right, report"
        )
    return SIMPLE_COMMANDS[cmd](robot)


class SimpleCommandsTranslatorFactory:
    """
    The command translator factory for building these command without arguments, such as: MoveCommandTranslator,
    LeftCommandTranslator, RightCommandTranslator, etc.
    This factory can build the command translator classes according to SIMPLE_COMMANDS, if you want to create a new
    simple command translator, please add the command information to SIMPLE_COMMANDS
    """

    @classmethod
    def build(cls) -> List[CommandTranslator]:
        """
        Do build the command translator classes based on SIMPLE_COMMANDS
        :return: a list of command translator classes
        """
        command_translators: List[CommandTranslator] = []
        for cmd in SIMPLE_COMMANDS:
            class_name = f"{cmd[0]}{cmd[1:].lower()}CommandTranslator"
            translator_class = cast(
                CommandTranslator, new_class(class_name, (CommandTranslator,))
            )
            translator_class.command = cmd
            setattr(translator_class, "translate", classmethod(translate))
            command_translators.append(translator_class)
        return command_translators


class PlaceCommandTranslator(CommandTranslator):
    """
    PlaceCommand translator, to translate string typed PLACE command into PlaceCommand object
    """

    command = "PLACE"

    @classmethod
    def translate(cls, robot: RobotPrototype, *args) -> PlaceCommand:
        if len(args) != 1:
            raise CommandError(
                "Place command must have args and args string should be the second "
                "argument and separated by ',' such as 'PLACE 0,0,NORTH'"
            )
        arguments = args[0].split(",")
        return PlaceCommandTranslator._translate_place_command(robot, arguments)

    @staticmethod
    def _translate_place_command(robot: RobotPrototype, arguments: List[str]):
        if len(arguments) != 3:
            raise CommandError(
                "PLACE command should has 3 args, represent 'x,y,FACING', such as '0,0,NORTH'"
            )
        x, y, facing = arguments[0], arguments[1], arguments[2]

        try:
            return PlaceCommand(robot, int(x), int(y), Facing[facing.upper()])
        except ValueError as e:
            raise CommandError(
                "PLACE command x and y arguments must be integers"
            ) from e
        except KeyError as e:
            raise CommandError(
                f"PLACE command facing argument must be in {[f.name for f in Facing]}"
            ) from e


class CommandsInterpreter:
    """
    A command interpreter for a robot
    """

    def __init__(self, robot: RobotPrototype):
        self.translators: dict = {}
        self.robot = robot
        self._register_default_translators()

    def interpret(self, command_list: List[str]) -> List[Command]:
        """
        Interpret a bunch of string typed commands into concrete Command objects
        :param command_list:  a bunch of string typed commands
        :return: list of concrete Command objects
        """
        commands: List[Command] = []
        for command_text in command_list:
            command = self._interpret_one_command(command_text)
            if command:
                commands.append(command)
        return commands

    def _interpret_one_command(self, command_text: str) -> Optional[Command]:
        command_and_args = command_text.strip().split(" ")
        if command_and_args and command_and_args[0]:
            cmd = command_and_args[0].upper()
            args = []
            if len(command_and_args) > 1:
                args = command_and_args[1:]

            if cmd not in self.translators:
                raise CommandError(
                    f"Unsupported command of {cmd}, supported commands: {list(self.translators)}"
                )
            return self.translators[cmd].translate(self.robot, *args)
        return None

    def _register_default_translators(self):
        SimpleCommandsTranslatorFactory.build()
        for translator_class in CommandTranslator.__subclasses__():
            self.translators[translator_class.command] = translator_class

    def register_translators(self, translator_class: Type[CommandTranslator]):
        """
        Register a new command translator
        :param translator_class: translator class
        :return:
        """
        self.translators[translator_class.command] = translator_class
