import sys
from typing import Literal
from unittest.mock import Mock

import pytest

from core.task_cli import get_supported_commands, get_target, main

EXPECTED_COMMANDS = {"add", "delete", "update", "mark", "list"}


@pytest.fixture
def mock_task_manager():
    manager = Mock()
    manager.save_data = Mock()
    for cmd in EXPECTED_COMMANDS:
        setattr(manager, cmd, Mock())
    return manager


def test_get_supported_commands(mock_task_manager: Mock):
    commands = get_supported_commands(mock_task_manager)
    assert set(commands.keys()) == EXPECTED_COMMANDS
    for cmd, props in commands.items():
        assert "target" in props and callable(props["target"])
        assert "help" in props and isinstance(props["help"], str)
        assert "args" in props and isinstance(props["args"], list)


@pytest.mark.parametrize(
    "cli_args, expected_cmd, expected_args",
    [
        (["add", "A new task"], "add", {"description": "A new task"}),
        (["delete", "3"], "delete", {"id": "3"}),
        (["update", "3", "Updated"], "update", {"id": "3", "description": "Updated"}),
        (["mark", "3", "in-progress"], "mark", {"id": "3", "status": "in-progress"}),
        (["mark", "3", "done"], "mark", {"id": "3", "status": "done"}),
        (["list"], "list", {"status": "all"}),
        (["list", "todo"], "list", {"status": "todo"}),
        (["list", "in-progress"], "list", {"status": "in-progress"}),
        (["list", "done"], "list", {"status": "done"}),
    ],
)
def test_get_target(
    monkeypatch: pytest.MonkeyPatch,
    mock_task_manager: Mock,
    cli_args: list[str],
    expected_cmd: Literal["add", "delete", "update", "mark", "list"],
    expected_args: dict[str, str],
):
    monkeypatch.setattr(sys, "argv", ["cli.py"] + cli_args)
    target, args = get_target(mock_task_manager)
    commands = get_supported_commands(mock_task_manager)
    expected_target = commands[expected_cmd]["target"]
    assert target == expected_target
    assert args == expected_args


def test_main_success(monkeypatch: pytest.MonkeyPatch, mock_task_manager: Mock):
    monkeypatch.setattr(
        "core.task_cli.TaskManager",
        lambda save_dir, data_file, id_file: mock_task_manager,
    )
    monkeypatch.setattr(sys, "argv", ["cli.py", "add", "Test task"])
    main()
    mock_task_manager.add.assert_called_once_with(description="Test task")
    mock_task_manager.save_data.assert_called_once()


def test_main_keyerror(monkeypatch, mock_task_manager):
    # Replace the 'add' command target with a function that always raises KeyError
    def failing_command(*args, **kwargs):
        raise KeyError("Simulated error")

    commands = get_supported_commands(mock_task_manager)
    commands["add"]["target"] = failing_command
    monkeypatch.setattr("core.task_cli.get_supported_commands", lambda task_manager: commands)  # fmt: skip
    monkeypatch.setattr("core.task_cli.TaskManager", mock_task_manager)
    monkeypatch.setattr(sys, "argv", ["cli.py", "add", "Error"])

    with pytest.raises(SystemExit) as excinfo:
        main()

    assert "No task ID found" in str(excinfo.value)
