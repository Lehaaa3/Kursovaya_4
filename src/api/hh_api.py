import requests
from src.api.base_api import BaseAPI
import json


class HeadHunterAPI(BaseAPI):
    """Класс для запроса вакансий на HeadHunter API"""

    url: str = 'https://api.hh.ru/vacancies'

    def __init__(self, url: str = url):
        """
        Инициализация класса HeadHunterAPI.

        :param url: URL для запросов к HeadHunter API.
        """
        super().__init__(url)

    def search_vacancies(self, job_title: str) -> list:
        """
        Поиск вакансий на HeadHunter API.

        :param job_title: Заголовок вакансии для поиска.
        :return: Список найденных вакансий.
        """
        params = {
            'text': job_title,
            'per_page': self._number_of_vacancies,
            'only_with_salary': True,
            'employment': 'full'
        }

        response = requests.get(url=self._base_url, params=params)
        response_json = response.json()

        return response_json.get("items", [])


