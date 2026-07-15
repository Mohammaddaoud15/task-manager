# Task Manager CLI

A simple command-line Task Manager built in Python that stores tasks in a JSON file. The project demonstrates modern Python development practices, including dataclasses, enums, dependency injection, configuration management, logging, unit testing, and a clean project structure.

## Features

- Create new tasks
- List all tasks
- Filter tasks by status
- Mark tasks as completed
- Delete tasks
- Store tasks in a JSON file
- Configurable storage path and log level
- Structured logging
- Unit tests with pytest
- Clean layered architecture

## Technologies Used

- Python 3.13+
- argparse
- dataclasses
- pathlib
- logging
- JSON
- pydantic-settings
- pytest
- uv

## Project Structure

```text
task-manager/
│
├── src/
│   └── task_manager/
│       ├── cli.py
│       ├── config.py
│       ├── exceptions.py
│       ├── models.py
│       ├── service.py
│       └── storage.py
│
├── tests/
│
├── pyproject.toml
└── README.md
```

## Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/task-manager.git
cd task-manager
```

Install dependencies

```bash
uv sync
```

Activate the virtual environment

Windows

```powershell
.venv\Scripts\Activate.ps1
```

Linux / macOS

```bash
source .venv/bin/activate
```

## Usage

Create a task

```bash
task-manager add "Study Python"
```

List tasks

```bash
task-manager list
```

List only completed tasks

```bash
task-manager list --status done
```

Mark a task as completed

```bash
task-manager complete <task_id>
```

Delete a task

```bash
task-manager delete <task_id>
```

## Running Tests

```bash
uv run pytest
```

## What I Learned

This project helped me practice:

- Object-oriented programming
- Dataclasses and Enums
- JSON serialization
- Context managers
- Custom exceptions
- Dependency Injection
- Configuration management
- Logging
- argparse
- Unit testing with pytest
- Mocking
- Clean Code principles
- Project organization
