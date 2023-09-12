from pycbrf import ExchangeRates
from datetime import datetime
from decimal import Decimal


def get_currency_data(currency: str) -> Decimal:
    """
    Получает данные о курсе заданной валюты.

    :param currency: Код валюты (например, 'USD', 'EUR', 'GBP').
    :return: Курс заданной валюты относительно рубля.
    """
    current_date = datetime.now().strftime('%Y-%m-%d')
    rates = ExchangeRates(current_date)
    currency = _check_currency(currency)
    currency_data = list(filter(lambda el: el.code == currency, rates.rates))[0].rate
    return Decimal(currency_data)


def _check_currency(currency: str) -> str:
    """
    Проверяет код валюты и возвращает его в правильном формате.

    :param currency: Код валюты.
    :return: Код валюты в правильном формате.
    """
    if currency == "BYR":
        return "BYN"
    return currency
