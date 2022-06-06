import pytest

from toy_robot.command_interpreter import (
    SimpleCommandsTranslatorFactory,
    PlaceCommandTranslator,
    CommandError,
)
from toy_robot.commands import (
    MoveCommand,
    LeftCommand,
    RightCommand,
    ReportCommand,
    PlaceCommand,
)
from toy_robot.models import Position, Facing


class TestSimpleCommandTranslatorFactory:
    def test_translate_simple_commands(self, robot):
        translator_classes = SimpleCommandsTranslatorFactory.build()
        assert len(translator_classes) == 4
        assert translator_classes[0].__name__ == "MoveCommandTranslator"
        assert translator_classes[1].__name__ == "LeftCommandTranslator"
        assert translator_classes[2].__name__ == "RightCommandTranslator"
        assert translator_classes[3].__name__ == "ReportCommandTranslator"

        cmd = translator_classes[0].translate(robot)
        assert isinstance(cmd, MoveCommand) is True

        cmd = translator_classes[1].translate(robot)
        assert isinstance(cmd, LeftCommand) is True

        cmd = translator_classes[2].translate(robot)
        assert isinstance(cmd, RightCommand) is True

        cmd = translator_classes[3].translate(robot)
        assert isinstance(cmd, ReportCommand) is True


class TestPlaceCommandTranslator:
    def test_translate_place_command(self, robot):
        cmd = PlaceCommandTranslator.translate(robot, "4,5,EAST")
        assert isinstance(cmd, PlaceCommand) is True
        assert cmd.position == Position(4, 5, Facing.EAST)

    def test_translate_when_invalid_arguments(self, robot):
        with pytest.raises(CommandError) as exc_info:
            PlaceCommandTranslator.translate(robot, "r,5,EAST", "33")
        assert exc_info.value.args[0] == (
            "Place command must have args and args string should be the second "
            "argument and separated by ',' such as 'PLACE 0,0,NORTH'"
        )

    def test_translate_when_invalid_arguments_format(self, robot):
        with pytest.raises(CommandError) as exc_info:
            PlaceCommandTranslator.translate(robot, "r,5 EAST")
        assert exc_info.value.args[0] == (
            "PLACE command should has 3 args, represent 'x,y,FACING', such as '0,0,NORTH'"
        )

    def test_translate_place_command_when_invalid_x(self, robot):
        with pytest.raises(CommandError) as exc_info:
            PlaceCommandTranslator.translate(robot, "r,5,EAST")
        assert (
            exc_info.value.args[0] == "PLACE command x and y arguments must be integers"
        )

    def test_translate_place_command_when_invalid_y(self, robot):
        with pytest.raises(CommandError) as exc_info:
            PlaceCommandTranslator.translate(robot, "1,o,EAST")
        assert (
            exc_info.value.args[0] == "PLACE command x and y arguments must be integers"
        )

    def test_translate_place_command_when_invalid_facing(self, robot):
        with pytest.raises(CommandError) as exc_info:
            PlaceCommandTranslator.translate(robot, "1,2,SOUTH_EAST")
        assert exc_info.value.args[0] == (
            "PLACE command facing argument must be in ['NORTH', 'EAST', 'SOUTH', 'WEST']"
        )


class TestCommandsInterpreter:
    def test_interpret_when_one_command(self, command_interpreter):
        commands = command_interpreter.interpret(["PLACE 0,0,EAST"])
        assert len(commands) == 1
        assert isinstance(commands[0], PlaceCommand) is True
        assert commands[0].position == Position(0, 0, Facing.EAST)

    def test_interpret_when_multiple_commands(self, command_interpreter):
        commands = command_interpreter.interpret(
            [" PLACE 0,0,EAST ", "moVe", "left", "Right", "report "]
        )
        assert len(commands) == 5
        assert isinstance(commands[0], PlaceCommand) is True
        assert isinstance(commands[1], MoveCommand) is True
        assert isinstance(commands[2], LeftCommand) is True
        assert isinstance(commands[3], RightCommand) is True
        assert isinstance(commands[4], ReportCommand) is True

    def test_interpret_when_empty_commands(self, command_interpreter):
        commands = command_interpreter.interpret([])
        assert len(commands) == 0

    def test_interpret_when_blank_commands(self, command_interpreter):
        commands = command_interpreter.interpret(["   "])
        assert len(commands) == 0

    def test_interpret_when_unsupported_command_test(self, command_interpreter):
        with pytest.raises(CommandError) as exc_info:
            command_interpreter.interpret(["JUMP", "1,2,SOUTH_EAST"])
        assert exc_info.value.args[0] == (
            "Unsupported command of JUMP, supported commands: ['PLACE', 'MOVE', 'LEFT', 'RIGHT', 'REPORT']"
        )

    def test_interpret_will_ignore_args_when_simple_command_has_args(
        self, command_interpreter
    ):
        move_command = command_interpreter.interpret(["MOVE 1,2,SOUTH_EAST"])
        assert isinstance(move_command[0], MoveCommand) is True
