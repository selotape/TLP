from datetime import datetime

import pytz

from TLP.configuration import LUNCH_TIME

jerusalem_timezone = pytz.timezone('Asia/Jerusalem')


def hour_in_israel(format_) -> str:
    return _datetime_in_israel().strftime(format_)


def _datetime_in_israel() -> datetime:
    return datetime.now(jerusalem_timezone)


def seconds_till_lunch_time():
    now = _datetime_in_israel()
    hour, minute = LUNCH_TIME.split(":")
    lunch_time = datetime(now.year, now.month, now.day, hour, minute, tzinfo=jerusalem_timezone)
    return (lunch_time - now).total_seconds()


def today():
    return datetime.now().date()
