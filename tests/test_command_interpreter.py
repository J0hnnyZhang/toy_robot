import pytest

from toy_robot.command_interpreter import SimpleCommandsTranslator, ArgumentCommandsTranslator, CommandError, \
    CommandsInterpreter
from toy_robot.commands import MoveCommand, LeftCommand, RightCommand, ReportCommand, PlaceCommand
from toy_robot.models import Position, Facing


class TestSimpleCommandTranslator:

    def test_translate_simple_commands(self, robot):
        cmd = SimpleCommandsTranslator.translate(robot, "move")
        assert isinstance(cmd, MoveCommand) is True

        cmd = SimpleCommandsTranslator.translate(robot, "left")
        assert isinstance(cmd, LeftCommand) is True

        cmd = SimpleCommandsTranslator.translate(robot, "right")
        assert isinstance(cmd, RightCommand) is True

        cmd = SimpleCommandsTranslator.translate(robot, "report")
        assert isinstance(cmd, ReportCommand) is True

    def test_translate_move_command_when_invalid_command_text(self, robot):
        with pytest.raises(CommandError) as exc_info:
            SimpleCommandsTranslator.translate(robot, "Back")
        assert exc_info.value.args[0] == (
            "Unsupported command of BACK, supported simple commands: move, left, right, report"
        )

    def test_translate_move_command_when_invalid_inputs(self, robot):
        with pytest.raises(CommandError) as exc_info:
            SimpleCommandsTranslator.translate(robot, "Back", "1")
        assert exc_info.value.args[0] == "Simple commands should not have args"


class TestArgumentCommandTranslator:
    def test_translate_place_command(self, robot):
        cmd = ArgumentCommandsTranslator.translate(robot, "Place", "4,5,EAST")
        assert isinstance(cmd, PlaceCommand) is True
        assert cmd.position == Position(4, 5, Facing.EAST)

    def test_translate_when_invalid_arguments(self, robot):
        with pytest.raises(CommandError) as exc_info:
            ArgumentCommandsTranslator.translate(robot, "Place", "r,5,EAST", "33")
        assert exc_info.value.args[0] == (
            "Argument commands must have args and args string should be the second "
            "argument, and multiple arguments should be separated by ',' such as 'PLACE 0,0,NORTH'"
        )

    def test_translate_when_invalid_arguments_format(self, robot):
        with pytest.raises(CommandError) as exc_info:
            ArgumentCommandsTranslator.translate(robot, "Place", "r,5 EAST")
        assert exc_info.value.args[0] == (
            "PLACE command should has 3 args, represent 'x,y,FACING', such as '0,0,NORTH'"
        )

    def test_translate_place_command_when_invalid_x(self, robot):
        with pytest.raises(CommandError) as exc_info:
            ArgumentCommandsTranslator.translate(robot, "Place", "r,5,EAST")
        assert exc_info.value.args[0] == "PLACE command x and y arguments must be integers"

    def test_translate_place_command_when_invalid_y(self, robot):
        with pytest.raises(CommandError) as exc_info:
            ArgumentCommandsTranslator.translate(robot, "Place", "1,o,EAST")
        assert exc_info.value.args[0] == "PLACE command x and y arguments must be integers"

    def test_translate_place_command_when_invalid_facing(self, robot):
        with pytest.raises(CommandError) as exc_info:
            ArgumentCommandsTranslator.translate(robot, "Place", "1,2,SOUTH_EAST")
        assert exc_info.value.args[0] == (
            "PLACE command facing argument must be in ['NORTH', 'EAST', 'SOUTH', 'WEST']"
        )

    def test_translate_when_unsupported_command_test(self, robot):
        with pytest.raises(CommandError) as exc_info:
            ArgumentCommandsTranslator.translate(robot, "jump", "1,2,SOUTH_EAST")
        assert exc_info.value.args[0] == (
            "Unsupported command of JUMP, supported argument commands: PLACE, such as 'PLACE 0,0,NORTH'"
        )


class TestCommandsInterpreter:
    def test_interpret_when_one_command(self, robot):
        ci = CommandsInterpreter(robot)
        commands = ci.interpret(["PLACE 0,0,EAST"])
        assert len(commands) == 1
        assert isinstance(commands[0], PlaceCommand) is True
        assert commands[0].position == Position(0, 0, Facing.EAST)

    def test_interpret_when_multiple_commands(self, robot):
        ci = CommandsInterpreter(robot)
        commands = ci.interpret(["PLACE 0,0,EAST", "moVe", "left", "Right", "report"])
        assert len(commands) == 5
        assert isinstance(commands[0], PlaceCommand) is True
        assert isinstance(commands[1], MoveCommand) is True
        assert isinstance(commands[2], LeftCommand) is True
        assert isinstance(commands[3], RightCommand) is True
        assert isinstance(commands[4], ReportCommand) is True

    def test_interpret_when_empty_commands(self, robot):
        ci = CommandsInterpreter(robot)
        commands = ci.interpret([])
        assert len(commands) == 0

    def test_interpret_when_blank_commands(self, robot):
        ci = CommandsInterpreter(robot)
        with pytest.raises(CommandError) as exc_info:
            ci.interpret(["   "])
        assert exc_info.value.args[0] == (
            "Argument commands must have args and args string should be the second argument, "
            "and multiple arguments should be separated by ',' such as 'PLACE 0,0,NORTH'"
        )
