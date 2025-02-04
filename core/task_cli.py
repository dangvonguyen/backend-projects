import sys
from argparse import ArgumentParser

from core.manager import TaskManager
from core.settings import *


def main():
    task_manager = TaskManager(SAVE_DIR, DATA_FILE, ID_FILE)

    target, args = get_target(task_manager)

    try:
        target(**args)
    except KeyError:
        sys.exit("No task ID found")

    task_manager.save_data()


def get_supported_commands(task_manager: TaskManager) -> dict[str, dict]:
    return {
        "add": {
            "target": task_manager.add,
            "help": "Add a new task with a description.",
            "args": [
                {
                    "name_or_flags": ["description"],
                    "help": "The description of the task.",
                }
            ],
        },
        "delete": {
            "target": task_manager.delete,
            "help": "Delete a task by its ID.",
            "args": [
                {
                    "name_or_flags": ["id"],
                    "help": "ID of the task to delete.",
                }
            ],
        },
        "update": {
            "target": task_manager.update,
            "help": "Update the description of an existing task.",
            "args": [
                {
                    "name_or_flags": ["id"],
                    "help": "ID of the task to update.",
                },
                {
                    "name_or_flags": ["description"],
                    "help": "New description for the task.",
                },
            ],
        },
        "mark": {
            "target": task_manager.mark,
            "help": "Mark a task with a new status.",
            "args": [
                {
                    "name_or_flags": ["id"],
                    "help": "ID of the task to update.",
                },
                {
                    "name_or_flags": ["status"],
                    "help": "New status to set for the task.",
                    "choices": ["in-progress", "done"],
                },
            ],
        },
        "list": {
            "target": task_manager.list,
            "help": "List tasks filtered by status.",
            "args": [
                {
                    "name_or_flags": ["status"],
                    "help": "Filter tasks by status.",
                    "nargs": "?",
                    "choices": ["all", "todo", "in-progress", "done"],
                    "default": "all",
                }
            ],
        },
    }


def get_target(task_manager: TaskManager):
    parser = ArgumentParser(
        description="A CLI application to track and manage your tasks"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    supported_commands = get_supported_commands(task_manager)
    for name, properties in supported_commands.items():
        new_parser = subparsers.add_parser(name, help=properties["help"])
        for arg in properties["args"]:
            new_parser.add_argument(*arg.pop("name_or_flags"), **arg)

    args = parser.parse_args().__dict__
    target = supported_commands[args.pop("command")]["target"]

    return target, args


if __name__ == "__main__":
    main()
