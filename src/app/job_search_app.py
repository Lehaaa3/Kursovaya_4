from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Optional, List

from src.api.hh_api import HeadHunterAPI
from src.api.super_job_api import SuperJobAPI
from src.file_handler.json_file_handler import JSONFileHandler
from src.file_handler.csv_file_handler import CSVFileHandler
from src.models.vacancy import Vacancy
from src.utils.сurrency_сonverter import get_currency_data
from src.app.job_search_meta import JobSearchAppMeta


class JobSearchApp(metaclass=JobSearchAppMeta):
    __vacancies: List[Vacancy] = []
    __hh_api: HeadHunterAPI = HeadHunterAPI()
    __superjob_api: SuperJobAPI = SuperJobAPI()
    __json_file_handler: JSONFileHandler = JSONFileHandler("json_vacancies.json")
    __csv_file_handler: CSVFileHandler = CSVFileHandler("csv_vacancies.csv")
    __job_title: Optional[str] = None
    __amount_vacancy: Optional[int] = None

    @classmethod
    def _interact_with_user(cls) -> None:
        """ Взаимодействие с пользователем. """
        while True:
            print("1. Поиск вакансий")
            print("2. Отобразить вакансии")
            print("3. Сохранить вакансии в файл")
            print("4. Выход")
            choice_menu = input("Выберите действие: ")

            if choice_menu == "1":
                cls.__job_title = input("Введите должность для поиска: ")
                cls.__search_vacancies()
                cls.__amount_vacancy = int(input("Введите сколько ТОП вакансий нужно: "))
                while True:
                    print("1. Сортировка по дате")
                    print("2. Сортировка по окладу")
                    choice_sorted = input("Выберите сортировку: ")
                    if choice_sorted == "1":
                        cls.__sorted_vacancy_for_date()
                        break
                    elif choice_sorted == "2":
                        cls.__sorted_vacancy_for_salary()
                        break
                    else:
                        print("Неверный выбор. Попробуйте еще раз.")
            elif choice_menu == "2":
                cls.__display_vacancies()
            elif choice_menu == "3":
                if cls.__vacancies:
                    cls.__save_vacancies_to_files()
                    print("Вакансии сохранены в файл.")
                else:
                    print("Нет доступных вакансий для сохранения.")
            elif choice_menu == "4":
                exit()
            else:
                print("Неверный выбор. Попробуйте еще раз.")

    @classmethod
    def __search_vacancies(cls) -> None:
        """Поиск вакансий."""
        with ThreadPoolExecutor() as executor:
            hh_future = executor.submit(cls.__hh_api.search_vacancies, cls.__job_title)
            sj_future = executor.submit(cls.__superjob_api.search_vacancies, cls.__job_title)
            hh_vacancies = hh_future.result()
            sj_vacancies = sj_future.result()
            for vacancy_data in hh_vacancies + sj_vacancies:
                title = cls.__get_title(vacancy_data)
                link = cls.__get_link(vacancy_data)
                salary_from = cls.__get_salary(vacancy_data)
                date_published = cls.__get_date_published(vacancy_data)
                currency = cls.__get_currency(vacancy_data)
                cls.__check_currency(title, link, salary_from, date_published, currency)

        return cls.__filtered_vacancies()

    @staticmethod
    def __get_title(vacancy) -> str:
        """Получение названия вакансии."""
        return vacancy["profession"] if vacancy.get("profession") is not None else vacancy["name"]

    @staticmethod
    def __get_link(vacancy) -> str:
        """Получение ссылки на вакансию."""
        return vacancy["link"] if vacancy.get("link") is not None else vacancy["alternate_url"]

    @staticmethod
    def __get_salary(vacancy) -> int:
        """Получение зарплаты от вакансии."""
        return vacancy["payment_from"] if vacancy.get("payment_from") is not None else vacancy["salary"]["from"]

    @staticmethod
    def __get_date_published(vacancy) -> str:
        """Получение даты публикации вакансии."""
        return datetime.utcfromtimestamp(vacancy["date_published"]).strftime('%Y.%m.%d') if vacancy.get(
            "date_published") is not None else vacancy["published_at"][:10]

    @staticmethod
    def __get_currency(vacancy) -> str:
        """Получение валюты вакансии."""
        return vacancy["currency"].upper() if vacancy.get("currency") else vacancy["salary"]["currency"].upper()

    @classmethod
    def __check_currency(cls, title, link, salary, date, currency) -> None:
        """Проверка и преобразование валюты, и добавление вакансии в список вакансий."""
        if currency not in ["RUR", "RUB"] and salary:
            salary *= get_currency_data(currency)
        if salary:
            cls.__vacancies.append(Vacancy(title, link, salary, date))

    @classmethod
    def __display_vacancies(cls) -> None:
        """Отображение вакансий"""
        if cls.__vacancies:
            print("Вакансии:")
            [print(vacancy) for vacancy in cls.__vacancies]
        else:
            print("Нет доступных вакансий.")

    @classmethod
    def __filtered_vacancies(cls) -> None:
        """Фильтрация вакансий по названию профессии"""
        cls.__vacancies = list(filter(lambda x: cls.__job_title.lower() in x.title.lower() and x.salary is not None,
                                      cls.__vacancies))

    @classmethod
    def __sorted_vacancy_for_salary(cls) -> None:
        """Сортировка вакансий по окладу."""
        if cls.__amount_vacancy > len(cls.__vacancies):
            print(f"К сожалению всего найдено вакансий: {len(cls.__vacancies)}")
        cls.__vacancies = sorted(cls.__vacancies, key=lambda x: x.salary, reverse=True)[
                          :cls.__amount_vacancy]

    @classmethod
    def __sorted_vacancy_for_date(cls) -> None:
        """Сортировка вакансий по дате публикации."""
        if cls.__amount_vacancy > len(cls.__vacancies):
            print(f"К сожалению всего найдено вакансий: {len(cls.__vacancies)}")
        cls.__vacancies = sorted(cls.__vacancies, key=lambda x: x.date, reverse=True)[
                          :cls.__amount_vacancy]

    @classmethod
    def __save_vacancies_to_files(cls) -> None:
        """Сохранения вакансий в JSON и CSV файлы."""
        for vacancy in cls.__vacancies:
            cls.__json_file_handler.add_vacancy(vacancy)
            cls.__csv_file_handler.add_vacancy(vacancy)

a = JobSearchApp()
a._interact_with_user()