from typing import Optional

from toy_robot.models import Position, Navigator


class Robot:
    def __init__(self, navigator: Navigator, position: Optional[Position] = None):
        self.current_position: Optional[Position] = None
        self.navigator: Navigator = navigator

        if position:
            self.set_position(position)

    def set_position(self, position: Position) -> None:
        self.current_position = position

    def turn_left(self) -> None:
        self.current_position.change_facing_to("left")

    def turn_right(self) -> None:
        self.current_position.change_facing_to("right")

    def move_forward(self) -> None:
        position = self.current_position.front()
        if self.navigator.safe(position):
            self.current_position = position
        else:
            print(f"This movement may endanger the robot, refuse to move")

    def report(self) -> None:
        print(f"Output: {self.current_position}")
