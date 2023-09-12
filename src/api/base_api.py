from abc import ABC, abstractmethod


class BaseAPI(ABC):
    def __init__(self, base_url: str, number_of_vacancies: int = 100):
        """
        Инициализация базового класса для API.

        :param base_url: Базовый URL для API.
        :param number_of_vacancies: Количество вакансий для получения.
        """
        self._base_url = base_url
        self._number_of_vacancies = number_of_vacancies

    @abstractmethod
    def search_vacancies(self, job_title: str) -> list:
        """
        Метод для поиска вакансий.

        :param job_title: Заголовок вакансии.
        :return: Список найденных вакансий.
        """
        pass
