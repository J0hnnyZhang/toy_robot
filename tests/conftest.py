import pytest

from toy_robot.command_interpreter import CommandsInterpreter
from toy_robot.models import Navigator, Table, Position, Facing
from toy_robot.robot import Robot


@pytest.fixture
def robot() -> Robot:
    navigator = Navigator(Table())
    return Robot(navigator, Position(0, 0, Facing.NORTH))


@pytest.fixture
def command_interpreter(robot):
    return CommandsInterpreter(robot)
