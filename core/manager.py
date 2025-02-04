import json
import os
from datetime import datetime
from typing import Literal

from tabulate import tabulate


class TaskManager:

    def __init__(self, save_dir: str, data_file: str, id_file: str):
        self.save_dir = save_dir
        self.data_path = os.path.join(save_dir, data_file)
        self.id_path = os.path.join(save_dir, id_file)
        self.data = self._load_data()
        self.current_id = self._load_id()

    def add(self, description: str) -> None:
        created_time = datetime.now().isoformat()
        self.current_id = new_id = self.current_id + 1
        self.data[str(new_id)] = {
            "description": description,
            "status": "todo",
            "created-at": created_time,
            "updated-at": created_time,
        }
        print(f"Task added successfully (ID: {new_id})")

    def delete(self, id: str) -> None:
        del self.data[id]

    def update(self, id: str, description: str) -> None:
        self.data[id]["description"] = description
        self.data[id]["updated-at"] = datetime.now().isoformat()

    def mark(self, id: str, status: Literal["in-progress", "done"]) -> None:
        self.data[id]["status"] = status
        self.data[id]["updated-at"] = datetime.now().isoformat()

    def list(
        self, status: Literal["all", "todo", "in-progress", "done"] = "all"
    ) -> None:
        DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"

        tabular_data = (
            {
                "ID": id,
                "Description": properties["description"],
                "Status": properties["status"],
                "Created At": datetime.fromisoformat(properties["created-at"]).strftime(
                    DATETIME_FORMAT
                ),
                "Updated At": datetime.fromisoformat(properties["updated-at"]).strftime(
                    DATETIME_FORMAT
                ),
            }
            for id, properties in sorted(self.data.items(), key=lambda x: x[0])
            if status == "all" or status == properties["status"]
        )

        print(
            tabulate(tabular_data, headers="keys", tablefmt="simple_grid")
            or "No items to display."
        )

    def _load_data(self) -> dict[str, dict]:
        try:
            with open(self.data_path, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        return data

    def _load_id(self) -> int:
        try:
            with open(self.id_path, "r") as f:
                id = int(f.read())
        except FileNotFoundError:
            id = 0
        return id

    def save_data(self) -> None:
        os.makedirs(self.save_dir, exist_ok=True)

        with open(self.data_path, "w") as f:
            json.dump(self.data, f, indent=4)

        with open(self.id_path, "w") as f:
            f.write(str(self.current_id))
