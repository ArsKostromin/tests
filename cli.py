from models import Task
from repository import JSONRepository
from services import TaskService

def main():
    repository = JSONRepository()
    service = TaskService(repository)

    while True:
        print("\nМеню:")
        print("1: Просмотреть задачи")
        print("2: Добавить задачу")
        print("3: Найти задачи")
        print("4: Изменить статус задачи")
        print("5: Удалить задачу")
        print("6: Выход")

        choice = input("Выберите действие: ")
        
        if choice == "1":
            service.get_all_tasks()


        elif choice == "2":
            title = input("Название: ")
            description = input("Описание: ")
            due_date = input("Срок выполнения (YYYY-MM-DD): ")
            priority = input("Приоритет (Низкий, Средний, Высокий): ").strip()
            task = Task(title=title, description=description, due_date=due_date, priority=priority)
            service.add_task(task)

        elif choice == "3":
            id_input = input("Введите id задачи или оставьте поле пустым: ")
            id = int(id_input) if id_input.strip() else None
            title = input("Название (или оставьте пустым): ") or None
            description = input("Введите описание (или оставьте пустым): ") or None
            due_date = input("Введите дату задачи (оставьте пустым для пропуска): ") or None
            service.find_tasks(id=id, title = title, description = description, due_date = due_date)
      

        elif choice == "4":
            task_id = int(input("ID задачи: "))
            status = input("Новый статус (Выполнено/Не выполнена): ").strip()
            if service.update_task_status(task_id, status):
                print("Статус обновлен.")
            else:
                print("Задача не найдена.")

        elif choice == "5":
            task_id = int(input("ID задачи: "))
            if service.delete_task(task_id):
                print("Задача удалена.")
            else:
                print("Задача не найдена.")

        elif choice == "6":
            print("Выход.")
            break

        else:
            print("Некорректный ввод.")


main()
