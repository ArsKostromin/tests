import pytest
from datetime import datetime
from models import Task
from services import TaskService
import os
from repository import JSONRepository

def test_task_initialization():
    task = Task(title="Test Task", description="Description", due_date="2024-12-31", priority="средний", status="не выполнено")
    assert task.title == "Test Task"
    assert task.description == "Description"
    assert task.due_date == datetime(2024, 12, 31).date()
    assert task.priority == "средний"
    assert task.status == "не выполнено"

def test_task_invalid_date():
    with pytest.raises(ValueError):
        Task(title="Test Task", description="Description", due_date="invalid-date", priority="средний", status="не выполнена")


@pytest.fixture
def setup_manager():
    """Создаёт тестовый менеджер с временным файлом хранения"""
    test_file = "test_manager.json"
    repository = JSONRepository(file_path=test_file)
    manager = TaskService(repository)
    yield manager
    if os.path.exists(test_file):
        os.remove(test_file)

def test_add_task(setup_manager):
    manager = setup_manager
    task = Task(title="Test Task", description="Description", due_date="2024-12-31", priority="средний", status="не выполнено")
    manager.add_task(task)
    assert len(manager.tasks) == 1
    assert manager.tasks[0].title == "Test Task"

def test_delete_task(setup_manager):
    manager = setup_manager
    task = Task(title="Test Task", description="Description", due_date="2024-12-31", priority="средний", status="не выполнено")
    manager.add_task(task)
    task_id = manager.tasks[0].id
    manager.delete_task(task_id)
    assert len(manager.tasks) == 0

def test_update_task_status(setup_manager):
    manager = setup_manager
    task = Task(title="Test Task", description="Description", due_date="2024-12-31", priority="средний", status="не выполнено")
    manager.add_task(task)
    task_id = manager.tasks[0].id
    manager.update_task_status(task_id, 'выполнено')
    assert manager.tasks[0].status == 'выполнено'