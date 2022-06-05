import sys

from toy_robot.command_interpreter import CommandError
from toy_robot.models import Table, Navigator
from toy_robot.robot import Robot


def initialize_table() -> Table:
    table_size = input("Please input the table size, default size is 5x5: ")
    while 1:
        if table_size:
            try:
                table = Table(int(table_size), int(table_size))
                break
            except ValueError:
                table_size = input(
                    "Please input the table size, ensure the input is positive integer, default size is 5x5: "
                )
        else:
            table = Table()
            break
    return table


def initialize() -> Robot:
    print("Welcome to toy robot game! Choose a table size, then you can command the robot to move on the table.\n")
    table = initialize_table()
    return Robot(Navigator(table))


def play(robot: Robot):
    print(
        "\nPLACE command to set the robot position on the table;\n"
        "MOVE command to order the robot move one step forward;\n"
        "LEFT command to order the robot turn left;\n"
        "RIGHT command to order the robot turn right;\n"
        "REPORT command to order the robot report its current position;\n"
        "Ctrl+C or EOF to exit\n"
        "\nPlease input your command: "
    )
    try:
        while 1:
            command_text = input()
            if command_text == "EOF":
                break
            commands = command_text.splitlines()
            try:
                robot.await_orders(commands)
            except CommandError as e:
                print(e.args[0])
                print("Please retry a again.")
            except ValueError as e:
                print(e.args[0])
                print("Please retry a again.")
    except KeyboardInterrupt:
        print("\nBye, welcome to play next time.")


def interactive_mode():
    robot = initialize()
    play(robot)


def automatic_mode(commands_filepath: str):
    robot = Robot(Navigator(Table()))
    with open(commands_filepath, "r") as f:
        for line in f:
            robot.await_orders([line.strip()])


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        interactive_mode()
    else:
        automatic_mode(args[1])
