from pathlib import Path
from typing import Literal

import pytest

from core.manager import TaskManager


@pytest.fixture
def task_manager(tmp_path: Path):
    return TaskManager(str(tmp_path), data_file="tasks.json", id_file="id.txt")


def test_init(task_manager: TaskManager):
    assert isinstance(task_manager.data, dict)
    assert task_manager.current_id == 0


def test_add_task(task_manager: TaskManager):
    descriptions = ["Task 1", "Task 2", "Task 3", "Final task"]

    for task_id, description in enumerate(descriptions, start=1):
        task_manager.add(description)
        task_id = str(task_id)
        assert task_id in task_manager.data
        assert task_manager.data[task_id]["description"] == description
        assert task_manager.data[task_id]["status"] == "todo"
        assert "created-at" in task_manager.data[task_id]
        assert "updated-at" in task_manager.data[task_id]

    assert len(task_manager.data) == 4


def test_delete_task(task_manager: TaskManager):
    task_manager.add("Task 1")
    task_manager.add("Task 2")

    task_manager.delete("1")
    assert "1" not in task_manager.data

    with pytest.raises(KeyError):
        task_manager.delete(2)

    with pytest.raises(KeyError):
        task_manager.delete("1")


def test_update_task(task_manager: TaskManager):
    task_manager.add("Original description")
    original_task = task_manager.data["1"].copy()

    task_manager.update("1", "Updated description")
    updated_task = task_manager.data["1"]

    del original_task["description"]
    assert updated_task.pop("description") == "Updated description"
    assert updated_task.pop("updated-at") != original_task.pop("updated-at")
    assert updated_task == original_task

    with pytest.raises(KeyError):
        task_manager.update(1, "error")

    with pytest.raises(KeyError):
        task_manager.update("2", "error")


@pytest.mark.parametrize("status", ["in-progress", "done"])
def test_mark_task(
    task_manager: TaskManager,
    status: Literal["in-progress"] | Literal["done"],
):
    task_manager.add("Test task")
    original_task = task_manager.data["1"].copy()

    task_manager.mark("1", status)
    updated_task = task_manager.data["1"]

    del original_task["status"]
    assert updated_task.pop("status") == status
    assert updated_task.pop("updated-at") != original_task.pop("updated-at")
    assert updated_task == original_task

    with pytest.raises(KeyError):
        task_manager.mark(1, status)

    with pytest.raises(KeyError):
        task_manager.mark("2", status)


def test_list_tasks(task_manager: TaskManager, capsys: pytest.CaptureFixture[str]):
    task_manager.add("todo task")
    task_manager.add("in-progress task")
    task_manager.add("done task")

    task_manager.mark("2", "in-progress")
    task_manager.mark("3", "done")

    # Capture stdout
    task_manager.list()
    captured = capsys.readouterr()
    assert "todo task" in captured.out
    assert "in-progress task" in captured.out
    assert "done task" in captured.out

    # Test status filtering
    status_list = ["todo", "in-progress", "done"]

    for status in status_list:
        task_manager.list(status)
        captured = capsys.readouterr()

        for tmp_status in status_list:
            description = tmp_status + " task"
            if status == tmp_status:
                assert description in captured.out
            else:
                assert description not in captured.out
