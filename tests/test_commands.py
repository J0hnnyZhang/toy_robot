from unittest import mock

from toy_robot.commands import PlaceCommand, MoveCommand, LeftCommand, RightCommand, ReportCommand
from toy_robot.models import Facing, Position
from toy_robot.robot import Robot


def test_place_command(robot):
    with mock.patch.object(Robot, "set_position") as mocked_set_position:
        place_command = PlaceCommand(robot, 1, 2, Facing.EAST)
        place_command.execute()
        mocked_set_position.assert_called_with(Position(1, 2, Facing.EAST))


def test_move_command(robot):
    with mock.patch.object(Robot, "move_forward") as mocked_move_forward:
        move_command = MoveCommand(robot)
        move_command.execute()
        mocked_move_forward.assert_called_once()


def test_left_command(robot):
    with mock.patch.object(Robot, "turn_left") as mocked_turn_left:
        left_command = LeftCommand(robot)
        left_command.execute()
        mocked_turn_left.assert_called_once()


def test_right_command(robot):
    with mock.patch.object(Robot, "turn_right") as mocked_turn_right:
        right_command = RightCommand(robot)
        right_command.execute()
        mocked_turn_right.assert_called_once()


def test_report_command(robot):
    with mock.patch.object(Robot, "report") as mocked_report:
        report_command = ReportCommand(robot)
        report_command.execute()
        mocked_report.assert_called_once()
