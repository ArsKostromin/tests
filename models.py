from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Literal


class Task(BaseModel):
    id: int = Field(default_factory=id)
    title: str = Field(..., min_length=1, max_length=15, description="Назваеие задачи")
    description: str = Field(max_length=35, description="Описание задачи")
    due_date: date = Field(..., description="Срок выполнения задачи в формате YYYY-MM-DD")
    priority: Literal["низкий", "средний", "выскоий"] = Field("Средний", description='Приоритет задачи')
    status: Literal["не выполнено", "выполнено"] = Field('не выполнено', description="Статус задачи")

    #mode='before обозначает валидацию до обработки данных.
    @field_validator("due_date", mode="before")
    def parse_due_date(cls, value: str):
        try:
            # Преобразуем строку в дату
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Некорректный формат даты. Используйте 'YYYY-MM-DD'.")