import json
from typing import List, Dict, Optional
from datetime import datetime


class Task:
    def __init__(self, title: str, description: str, due_date: str, priority: str, status: str): #Инициализация 
        self.id = id(self)
        self.title = title
        self.description = description
        
        # дата из строки формата "YYYY-MM-DD"
        try:
            self.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError: # обработка невалидной даты
            raise ValueError("Некорректный формат даты. Используйте 'YYYY-MM-DD'.")
        
        self.status = status
        self.priority = priority
        

    def to_dict(self) -> Dict: #Преобразует объект задачи в словарь
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.strftime("%Y-%m-%d"),
            "status": self.status,
            "priority": self.priority
        }

    @classmethod #делает метод привязанным к классу, а не к конкретному экземпляру.
    def from_dict(cls, data: Dict):
        """Создаёт объект задачи из словаря."""
        task = cls(
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"],  # Дата в формате строки
            priority=data.get("priority", "Высокий"),
            status=data.get("status", "Не выполнена")
        )
        task.id = data.get("id", id(task))
        return task


class TaskManager:
    def __init__(self, storage_file: str = "Manager.json"): #Инициализация 
        self.storage_file = storage_file
        self.TaskManagers: List[Task] = self.load_TaskManagers() #список задач

    def load_TaskManagers(self) -> List[Task]:  #достаёт задачи из json
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Task.from_dict(TaskManager) for TaskManager in data] #преобразуем в объекты Task.
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_TaskManagers(self): # сохранение текущего состояния списка в файл json
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump([TaskManager.to_dict() for TaskManager in self.TaskManagers], file, ensure_ascii=False, indent=4)

    def add_TaskManager(self, title: str, description: str, due_date: str, priority: str, status: str,): #добавление задачи
        TaskManager = Task(title, description, due_date, priority, status,)
        self.TaskManagers.append(TaskManager)
        self.save_TaskManagers()
        print(f"Задача '{title}' добавлена с ID {TaskManager.id}.")

    def delete_TaskManager(self, TaskManager_id: int):
        TaskManager = self.find_TaskManager_by_id(TaskManager_id)
        if TaskManager:
            self.TaskManagers.remove(TaskManager)
            self.save_TaskManagers()
            print(f"Задача с ID {TaskManager_id} удалена.")
        else:
            print(f"Задача с ID {TaskManager_id} не найдена.")

    def find_TaskManagers(self, title: Optional[str] = None, description: Optional[str] = None, due_date: Optional[str] = None):
        results = [
            TaskManager
            for TaskManager in self.TaskManagers
            if (title is None or title.lower() in TaskManager.title.lower())
            and (description is None or description.lower() in TaskManager.description.lower())  
            and (due_date is None or due_date == TaskManager.due_date.strftime("%Y-%m-%d"))
        ]
        if results:
            for TaskManager in results:
                self.display_TaskManager(TaskManager)
        else:
            print("Задачи не найдены.")

    def display_TaskManagers(self):
        if not self.TaskManagers:
            print("Список пуст.")
        else:
            for TaskManager in self.TaskManagers:
                self.display_TaskManager(TaskManager)

    def change_TaskManager_status(self, TaskManager_id: int, new_status: str):
        TaskManager = self.find_TaskManager_by_id(TaskManager_id)
        if TaskManager:
            if new_status in ["выполнена", "Не выполнена"]:
                TaskManager.status = new_status
                self.save_TaskManagers()
                print(f"Статус задачи с ID {TaskManager_id} изменён на '{new_status}'.")
            else:
                print("Неверный статус. Используйте 'выполнена' или 'Не выполнена'.")
        else:
            print(f"Задача с ID {TaskManager_id} не найдена.")

    def find_TaskManager_by_id(self, TaskManager_id: int) -> Optional[Task]:
        return next((TaskManager for TaskManager in self.TaskManagers if TaskManager.id == TaskManager_id), None)

    @staticmethod
    def display_TaskManager(TaskManager: Task):
        print(f"ID: {TaskManager.id}, Title: {TaskManager.title}, description: {TaskManager.description}, due_date: {TaskManager.due_date}, Status: {TaskManager.status}, priority: {TaskManager.priority}")


def main():
    Manager = TaskManager()

    while True:
        print("\nВыберите действие:")
        print("1: Добавить задачу")
        print("2: Удалить задачу")
        print("3: Поиск задачи")
        print("4: Показать все задачи")
        print("5: Изменить статус задачи")
        print("6: Выход")
        choice = input("Введите номер действия: ")

        if choice == "1":
            title = input("Введите название задачи: ")
            if  title.strip()=='':
                print('Ошибка: Название задачи не может быть пустым.')
                break
            description = input("Введите описание задачи: ")
            if description.strip()=='':
                print('Ошибка: Описание задачи не может быть пустым.')
                break
            due_date = (input("Введите дату задачи: "))
            priority = (input("Введите приоритет:('Низкий', 'Средний', 'Высокий') "))
            if priority.lower() not in ['низкий', 'средний', 'высокий']:
                print('Ошибка: Приоритет задачи задан неверно.')
                break
            status = input("Введите статус(выполнено/Не выполнено): ")
            if status.lower() not in ['выполнено', 'не выполнено']:
                print('Ошибка: Сатус задачи задан неверно.')
                break
            
            Manager.add_TaskManager(title, description, due_date, priority, status)

        elif choice == "2":
            TaskManager_id = int(input("Введите ID задачи для удаления: "))
            Manager.delete_TaskManager(TaskManager_id)

        elif choice == "3":
            title = input("Введите название задачи (оставьте пустым для пропуска): ") or None
            description = input("Введите описание задачи (оставьте пустым для пропуска): ") or None
            due_date = input("Введите дату задачи (оставьте пустым для пропуска): ") or None
            Manager.find_TaskManagers(title, description, due_date)

        elif choice == "4":
            Manager.display_TaskManagers()

        elif choice == "5":
            TaskManager_id = int(input("Введите ID книги для изменения статуса: "))
            new_status = input("Введите новый статус ('выполнена' или 'Не выполнена'): ")
            Manager.change_TaskManager_status(TaskManager_id, new_status)

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Неверный ввод, попробуйте снова.")


if __name__ == "__main__":
    main()
