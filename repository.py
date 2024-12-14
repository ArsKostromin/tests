import json
from models import Task
from typing import List, Optional
from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def load(self) -> List[Task]:
        pass
    
    @abstractmethod
    def save(self, tasks: List[Task]) -> None:
        pass
    
class JSONRepository(AbstractRepository):
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = file_path
        
    def load(self) -> List[Task]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Task(**task) for task in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
    def save(self, tasks: List[Task]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([task.model_dump() for task in tasks], file, ensure_ascii=False, indent=4, default=str)
