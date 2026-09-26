from datetime import date


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число, повторяя запрос при ошибке."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число")


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате ДД.ММ.ГГГГ."""
    while True:
        raw_value = input(prompt)
        try:
            day, month, year = (int(part) for part in raw_value.split("."))
            return date(year, month, day)
        except ValueError:
            print("Введите дату в формате ДД.ММ.ГГГГ")
