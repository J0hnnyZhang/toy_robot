from unittest import TestCase, mock
from unittest.mock import MagicMock

from toy_robot.models import Facing, Navigator, Table
from toy_robot.robot import Robot, Position


class TestRobot(TestCase):

    def setUp(self) -> None:
        self.robot = Robot(Navigator(Table()), Position(0, 0, Facing.NORTH))

    def test_turn_left(self):
        with mock.patch.object(Position, "facing_left") as mocked_facing_left:
            robot = Robot(Navigator(Table()), Position(0, 0, Facing.NORTH))
            robot.turn_left()
            mocked_facing_left.assert_called_once()

    def test_turn_right(self):
        with mock.patch.object(Position, "facing_right") as mocked_facing_right:
            robot = Robot(Navigator(Table()), Position(0, 0, Facing.NORTH))
            robot.turn_right()
            mocked_facing_right.assert_called_once()

    def test_set_position(self):
        self.robot.set_position(Position(4, 2, Facing.NORTH))
        x, y, f = self.robot.current_position.x, self.robot.current_position.y, self.robot.current_position.f
        assert x == 4
        assert y == 2
        assert f == Facing.NORTH

    def test_move_forward_should_call_position_and_navigator(self):
        with (mock.patch.object(Position, "front") as mocked_front,
              mock.patch.object(Navigator, "safe") as mocked_safe):
            self.robot.move_forward()

            mocked_front.assert_called_once()
            mocked_safe.assert_called_once()

    def test_move_forward_when_safe_move(self):
        self.robot.set_position(Position(0, 0, Facing.NORTH))
        self.robot.move_forward()
        assert self.robot.current_position.x == 0
        assert self.robot.current_position.y == 1
