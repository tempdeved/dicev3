from datetime import datetime
from datetime import date


def CalculateAge(born):
    born = datetime.strptime(born, "%Y-%m-%d").date()
    # born = datetime.strptime(born, "%d/%m/%Y").date()
    today = date.today()

    anos = today.year - born.year - (
            (today.month, today.day) < (born.month, born.day)
    )

    meses = 12 - (born.month - today.month)

    result = f'{anos} anos {meses} meses'

    return result