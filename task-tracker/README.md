# Task Tracker CLI

A simple command-line interface (CLI) application to track and manage your tasks.

This project is based on the [Task Tracker CLI](https://roadmap.sh/projects/task-tracker) project from roadmap.sh.

## Features

- **Add** a new task with a description.
- **Delete** a task by its ID.
- **Update** a task's description.
- **Mark** a task with a new status (`in-progress` or `done`)
- **List** tasks with their status (`all`, `todo`, `in-progress` or `done`)

## Installation

### Clone the Repository

```bash
git clone https://github.com/dangvonguyen/backend-projects.git

# Navigate to the project directory
cd backend-projects/task-tracker
```

### Install the Package

```bash
pip install -e .
```

## Usage

After installation, use `task-cli` to manage tasks:

- `add`: Add a task

```bash
task-cli add <description>
```

- `delete`: Delete a task

```bash
task-cli delete <id>
```

- `update`: Update a task

```bash
task-cli update <id> <description>
```

- `mark`: Mark a task with a new status

```bash
task-cli update <id> <status>
```

- `list`: List tasks filtered by status

```bash
task-cli list [<status>]
```