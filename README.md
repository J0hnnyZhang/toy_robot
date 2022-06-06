# toy_robot

A code challenge

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

- add pre-commit hooks, **do this only when you want to contribute to this project**, then 
  - when you do `git commit`
  
    `black` and `pylint` will run, `black` to reformat the changed files and `pylint` to check if the change files are in
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

