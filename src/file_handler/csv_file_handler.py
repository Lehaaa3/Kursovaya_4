import csv
from typing import Dict, Any, List

from src.file_handler.base_file_handler import BaseFileHandler, Vacancy


class CSVFileHandler(BaseFileHandler):
    """Класс для обработки CSV файлов с вакансиями"""

    def __init__(self, file_path: str):
        """
        Инициализация объекта CSVFileHandler.

        :param file_path: Путь к CSV файлу.
        """
        self.file_path = file_path

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавляет вакансию в CSV файл.

        :param vacancy: Вакансия для добавления.
        """
        with open(self.file_path, "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                vacancy.title,
                vacancy.link,
                vacancy.salary,
                vacancy.date
            ])

    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Возвращает список вакансий из CSV файла, соответствующих заданным критериям.

        :param criteria: Критерии для выборки вакансий.
        :return: Список вакансий, соответствующих заданным критериям.
        """
        vacancies = []
        with open(self.file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                vacancy_data = {
                    "title": row[0],
                    "link": row[1],
                    "salary": row[2],
                    "date": row[3]
                }
                if self._vacancy_matches_criteria(vacancy_data, criteria):
                    vacancies.append(vacancy_data)
        return vacancies

    def remove_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удаляет вакансию из CSV файла.

        :param vacancy: Вакансия для удаления.
        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)
        with open(self.file_path, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(rows[0])
            for row in rows[1:]:
                vacancy_data = {
                    "title": row[0],
                    "link": row[1],
                    "salary": row[2],
                    "date": row[3]
                }
                if not self._vacancy_equals(vacancy_data, vacancy):
                    writer.writerow(row)

    @staticmethod
    def _vacancy_matches_criteria(vacancy_data: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """
        Проверяет, соответствует ли вакансия заданным критериям.

        :param vacancy_data: Данные вакансии.
        :param criteria: Критерии для проверки.
        :return: True, если вакансия соответствует критериям, иначе False.
        """
        for key, value in criteria.items():
            if key not in vacancy_data or vacancy_data[key] != value:
                return False
        return True

    @staticmethod
    def _vacancy_equals(vacancy_data1: Dict[str, Any], vacancy_data2: Dict[str, Any]) -> bool:
        """
        Проверяет, являются ли две вакансии одинаковыми.

        :param vacancy_data1: Данные первой вакансии.
        :param vacancy_data2: Данные второй вакансии.
        :return: True, если вакансии равны, иначе False.
        """
        return vacancy_data1 == vacancy_data2
