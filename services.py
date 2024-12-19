from typing import List, Optional
from models import Task
from repository import AbstractRepository

class TaskService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository
        self.tasks = self.repository.load()
        
    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
        self.repository.save(self.tasks)
        
    def get_all_tasks(self) -> List[Task]:
        if self.tasks:
         for task in self.tasks:
            print(f"ID: {task.id}", f"| Название: {task.title}", f"| Описание: {task.description}", f"| Срок выполнения: {task.due_date.strftime('%Y-%m-%d')}", f"| Приоритет: {task.priority}", f"| Статус: {task.status}")
        else:
            print("Задачи не найдены.")
    
    def find_tasks(self, id: Optional[int] = None, title: Optional[str] = None, description: Optional[str] = None, due_date: Optional[str] = None):
        results = [
            task
            for task in self.tasks
            if (title is None or title.lower() in task.title.lower())
            and (description is None or description.lower() in task.description.lower())  
            and (due_date is None or due_date == task.due_date.strftime("%Y-%m-%d"))
            and (id is None or id == task.id)
        ]
        
        if results:
            for task in results:
                print(f"ID: {task.id}")
                print(f"Название: {task.title}")
                print(f"Описание: {task.description}")
                print(f"Срок выполнения: {task.due_date.strftime('%Y-%m-%d')}")
                print(f"Приоритет: {task.priority}")
                print(f"Статус: {task.status}")
                print("\n")  # Разделение для удобства чтения
        else:
            print("Задачи не найдены.")
        
    def delete_task(self, task_id: int) -> bool:
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            self.tasks.remove(task)
            self.repository.save(self.tasks)
            return True
        return False
    
    def update_task_status(self, task_id: int, status: str) -> bool:
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            task.status = status
            self.repository.save(self.tasks)
            return True
        return False