from datetime import datetime

import pytz

from TLP.configuration import LUNCH_TIME

jerusalem_timezone = pytz.timezone('Asia/Jerusalem')


def datetime_in_israel() -> datetime:
    return jerusalem_timezone.localize(datetime.now())


def seconds_till_lunch_time():
    now = datetime_in_israel()
    hour, minute = LUNCH_TIME.split(":")
    lunch_time = jerusalem_timezone.localize(datetime(now.year, now.month, now.day, hour, minute))
    return (lunch_time - now).total_seconds()
