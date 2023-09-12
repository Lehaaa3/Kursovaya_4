from abc import ABC, abstractmethod
from typing import List

from src.models.vacancy import Vacancy


class BaseFileHandler(ABC):
    """Абстрактный базовый класс для обработки файлов"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Абстрактный метод для добавления вакансии в файл.

        :param vacancy: Вакансия для добавления.
        """
        pass

    @abstractmethod
    def get_vacancies(self, criteria: str) -> List[Vacancy]:
        """
        Абстрактный метод для получения вакансий из файла по заданным критериям.

        :param criteria: Критерии для выборки вакансий.
        :return: Список вакансий, соответствующих заданным критериям.
        """
        pass

    @abstractmethod
    def remove_vacancy(self, vacancy: Vacancy) -> None:
        """
        Абстрактный метод для удаления вакансии из файла.

        :param vacancy: Вакансия для удаления.
        """
        pass
