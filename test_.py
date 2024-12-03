import pytest
from datetime import datetime
from console import Task, TaskManager
import os

def test_task_initialization():
    task = Task("Test Task", "Description", "2024-12-31", "Высокий", "Не выполнена")
    assert task.title == "Test Task"
    assert task.description == "Description"
    assert task.due_date == datetime(2024, 12, 31).date()
    assert task.priority == "Высокий"
    assert task.status == "Не выполнена"

def test_task_invalid_date():
    with pytest.raises(ValueError):
        Task("Test Task", "Description", "invalid-date", "Высокий", "Не выполнена")


@pytest.fixture
def setup_manager():
    """Создаёт тестовый менеджер с временным файлом хранения"""
    test_file = "test_manager.json"
    manager = TaskManager(storage_file=test_file)
    yield manager
    if os.path.exists(test_file):
        os.remove(test_file)

def test_add_task(setup_manager):
    manager = setup_manager
    manager.add_TaskManager("Test Task", "Description", "2024-12-31", "Высокий", "Не выполнена")
    assert len(manager.TaskManagers) == 1
    assert manager.TaskManagers[0].title == "Test Task"

def test_delete_task(setup_manager):
    manager = setup_manager
    manager.add_TaskManager("Test Task", "Description", "2024-12-31", "Высокий", "Не выполнена")
    task_id = manager.TaskManagers[0].id
    manager.delete_TaskManager(task_id)
    assert len(manager.TaskManagers) == 0

