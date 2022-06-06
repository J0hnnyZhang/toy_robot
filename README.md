# toy_robot

This is an application which simulates a toy robot moving on a square table-top, 
There are no other obstructions on the table surface. The robot is free to roam around the surface of the table, 
but must be prevented from falling to destruction. Any movement that would result in the robot falling from the table 
must be prevented, however further valid movement commands must still be allowed.

The commands include:
- PLACE will put the toy robot on the table in position X,Y and facing NORTH, SOUTH, EAST or WEST. 
The origin (0,0) can be considered to be the SOUTH WEST most corner. It is required that the first command to the robot, after that, any sequence of commands may be issued, in any order, including another PLACE command. 
The application should discard all commands in the sequence until a valid PLACE command has been executed. 
- MOVE will move the toy robot one unit forward in the direction it is currently facing. 
- LEFT and RIGHT will rotate the robot 90 degrees in the specified direction without changing the position of the robot. 
- REPORT will announce the X,Y and F of the robot. This can be in any form, but standard output is sufficient. 

A robot that is not on the table can choose to ignore the MOVE, LEFT, RIGHT and REPORT commands. 
Input can be from a file, or from standard input.

## Quick setup

This project is based on Python 3.10.4 and only tested in Python 3.10.4, please make sure the Python version is
Python 3.10+. This project uses `poetry` to manage the dependencies and `pre-commit` to run the hooks for `black`,
`pylint` in code commit stage and `mypy` in code push stage.

- clone the code

```
git clone https://github.com/J0hnnyZhang/toy_robot.git
```

- create python virtual env

```
cd toy_robot
python -m venv venv
source venv/bin/activate
```

- install dependencies
  you can install through poetry

```
  poetry install
```

or install through pip

```
  pip install -r requirements.txt 
```

- run all tests
```
  pytest tests
```

- add pre-commit hooks, **do this only when you want to contribute to this project**, then 
  - when you do `git commit`
  
    `black` and `pylint` will run, `black` to reformat the changed files and `pylint` to check if the changed files are in
  good code style.
  - when do `git push`
   
    `mypy` will run to check if there are typing issues
```
pre-commit install
```

## How to run

Support two mode to run the application, interactively and automatically.

By interactively, the user can reset the table size and input the command one by one.

By automatically, the user can let the robot execute a bunch of commands from a file, in this mode the
user need to ensure the correction of the commands or the robot will refuse to execute the commands

### Interactively

```
python toyrobot/cli.py
```

### Automatically

```
python toyrobot/cli.py ${commands_file_python}
```

- such as, run the commands from `tests/resources/commands_01.txt

```
python toy_robot/cli.py tests/resources/commands_01.txt
```

### Probable issues

- "ModuleNotFoundError: No module named 'toy_robot'"
  
  You can fix it by add the toy_robot root directory to `PYTHONPATH`

```
cd toy_robot
export PYTHONPATH="${PYTHONPATH}:."
```

