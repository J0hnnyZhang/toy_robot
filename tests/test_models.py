from unittest import TestCase, mock

from toy_robot.models import Facing, Position, Table, Navigator


class TestFacing(TestCase):
    def test_left(self):
        assert Facing.NORTH.left() == Facing.WEST
        assert Facing.WEST.left() == Facing.SOUTH
        assert Facing.SOUTH.left() == Facing.EAST
        assert Facing.EAST.left() == Facing.NORTH

    def test_right(self):
        assert Facing.NORTH.right() == Facing.EAST
        assert Facing.WEST.right() == Facing.NORTH
        assert Facing.SOUTH.right() == Facing.WEST
        assert Facing.EAST.right() == Facing.SOUTH


class TestPosition(TestCase):
    def test_repr(self):
        assert f"{Position(2, 3, Facing.SOUTH)}" == "2,3,SOUTH"

    def test_eq(self):
        position1 = Position(2, 3, Facing.SOUTH)
        position2 = Position(2, 3, Facing.SOUTH)
        assert position1 == position2

    def test_front(self):
        position1 = Position(0, 0, Facing.NORTH)
        assert position1.front() == Position(0, 1, Facing.NORTH)

        position2 = Position(0, 0, Facing.WEST)
        assert position2.front() == Position(-1, 0, Facing.WEST)

        position3 = Position(0, 0, Facing.SOUTH)
        assert position3.front() == Position(0, -1, Facing.SOUTH)

        position4 = Position(0, 0, Facing.EAST)
        assert position4.front() == Position(1, 0, Facing.EAST)

    def test_change_facing(self):
        position = Position(0, 0, Facing.NORTH)
        position.change_facing(Facing.SOUTH)
        assert position.f == Facing.SOUTH

        facing_right = position.f.right()
        position.change_facing(facing_right)
        assert position.f == Facing.WEST

    def test_change_facing_to_when_origin_facing_is_north(self):
        position = Position(0, 0, Facing.NORTH)
        position.change_facing_to("right")
        assert position.f == Facing.EAST

        position.change_facing_to("LEFT")
        assert position.f == Facing.NORTH

    def test_change_facing_to_when_invalid_facing_direction(self):
        position = Position(0, 0, Facing.WEST)
        with self.assertRaises(NotImplementedError) as exc_info:
            position.change_facing_to("back")
        assert exc_info.exception.args[0] == "Invalid arguments, only 'left' and 'right' is allowed for now"


class TestTable(TestCase):
    def test_invalid_table_length(self):
        with self.assertRaises(ValueError) as exe_info:
            Table(-1, 1)
        assert exe_info.exception.args[0] == "A table should not has negative or zero value for length or width"

    def test_invalid_table_width(self):
        with self.assertRaises(ValueError) as exe_info:
            Table(5, 0)
        assert exe_info.exception.args[0] == "A table should not has negative or zero value for length or width"


class TestNavigator(TestCase):
    def setUp(self) -> None:
        self.navigator = Navigator(Table(5, 5))

    def test_safe_when_position_beyond_table_width(self):
        assert self.navigator.safe(Position(-1, 2, Facing.SOUTH)) is False
        assert self.navigator.safe(Position(5, 2, Facing.SOUTH)) is False

    def test_safe_when_position_beyond_table_length(self):
        assert self.navigator.safe(Position(3, -1, Facing.SOUTH)) is False
        assert self.navigator.safe(Position(1, 5, Facing.SOUTH)) is False

    def test_safe_when_a_safe_position(self):
        assert self.navigator.safe(Position(4, 4, Facing.SOUTH)) is True
        assert self.navigator.safe(Position(0, 0, Facing.SOUTH)) is True
        assert self.navigator.safe(Position(1, 2, Facing.SOUTH)) is True
