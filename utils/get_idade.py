from datetime import datetime
from datetime import date


def CalculateAge(born):
    today = datetime.now()
    try:
        birthday = born.replace(year=today.year)

    except ValueError:
        birthday = born.replace(year=today.year,
                                month=born.month + 1, day=1)

    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year