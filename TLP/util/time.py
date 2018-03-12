from datetime import datetime

import pytz

jerusalem_timezone = pytz.timezone('Asia/Jerusalem')


def datetime_in_israel() -> datetime:
    return jerusalem_timezone.localize(datetime.now())


def seconds_till_eleven_thirty():
    now = datetime_in_israel()
    eleven_thirty = jerusalem_timezone.localize(datetime(now.year, now.month, now.day, 11, 30))
    return (eleven_thirty - now).total_seconds()
