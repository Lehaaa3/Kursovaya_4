from functools import total_ordering
from typing import Union


@total_ordering
class Vacancy:
    """Класс, представляющий информацию о вакансии"""

    def __init__(self, title: str, link: str, salary: str, date: str):
        """
        Инициализация объекта Vacancy.

        :param title: Название вакансии.
        :param link: Ссылка на вакансию.
        :param salary: Зарплата.
        :param date: Дата размещения вакансии.
        """
        self.title = title
        self.link = link
        self.salary = salary
        self.date = date

    def __str__(self) -> str:
        """
        Возвращает строковое представление вакансии.

        :return: Строковое представление вакансии.
        """
        return f"Vacancy: {self.title}\nLink: {self.link}\nSalary: от {self.salary} руб.\nDate: {self.date}\n"

    def __repr__(self) -> str:
        """
        Возвращает представление вакансии в виде строки.

        :return: Представление вакансии в виде строки.
        """
        return f"Vacancy(title={self.title}, link={self.link}, salary={self.salary}, Date={self.date})"

    def __eq__(self, other: 'Vacancy') -> bool:
        """
        Проверяет, равны ли две вакансии по зарплате.

        :param other: Другая вакансия для сравнения.
        :return: True, если зарплаты равны, иначе False.
        """
        return self.salary == other.salary

    def __lt__(self, other: 'Vacancy') -> bool:
        """
        Определяет порядок сортировки вакансий по зарплате.

        :param other: Другая вакансия для сравнения.
        :return: True, если текущая вакансия имеет меньшую зарплату, иначе False.
        """
        return self.salary < other.salary

    @property
    def salary(self) -> int:
        """
        Возвращает зарплату вакансии.

        :return: Зарплата вакансии.
        """
        return self.__salary

    @salary.setter
    def salary(self, value: Union[int, float, str]) -> None:
        """
        Устанавливает зарплату вакансии.

        :param value: Значение зарплаты.
        """
        self.__salary = int(float(value))

    def validate_salary(self) -> bool:
        """
        Проверяет, является ли зарплата валидной.

        :return: True, если зарплата валидна, иначе False.
        """
        if isinstance(self.salary, (int, float)):
            return True
        elif isinstance(self.salary, str):
            salary_parts = self.salary.split('-')
            if len(salary_parts) == 2:
                min_salary, max_salary = salary_parts
                if min_salary.isdigit() and max_salary.isdigit():
                    return True
        return False

    def validate_data(self) -> bool:
        """
        Проверяет, являются ли все данные вакансии валидными.

        :return: True, если все данные валидны, иначе False.
        """
        if not all([self.title, self.link, self.salary, self.date]):
            return False
        return True
