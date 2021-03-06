import logging
from datetime import datetime

import wrapt
from boltons.iterutils import chunked
from frozendict import frozendict


def polite_chunk(todays_users, size):
    chunked_users = chunked(todays_users, size)
    if len(chunked_users) <= 1 or chunked_users[-1] == size:
        return chunked_users

    chunked_users, last_chunk = chunked_users[:-1], chunked_users[-1]
    for i, user in enumerate(last_chunk):
        chunked_users[i].append(user)
    return chunked_users


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def with_entry_log(log_method):
    @wrapt.decorator
    def wrapper(wrapped, _, args, kwargs):
        log_method(f'== calling {wrapped.__name__}')
        return wrapped(*args, **kwargs)

    return wrapper


class _DayCache:
    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)
        self._todays_cache = {}
        self._last_refresh_date = datetime.now().date()

    def _maybe_refresh_cache(self):
        today = datetime.now().date()
        if today > self._last_refresh_date:
            self._log.debug("refreshing cache")
            self._todays_cache = {}
            self._last_refresh_date = today

    @staticmethod
    def key(*args, **kwargs):
        return args, frozendict(**kwargs)

    @wrapt.decorator
    def __call__(self, wrapped, instance, args, kwargs):
        self._maybe_refresh_cache()

        key = _DayCache.key(*args, **kwargs)
        if key not in self._todays_cache:
            self._log.debug(f"Executing function '{wrapped.__name__}'")
            result = wrapped(*args, **kwargs)
            self._todays_cache[key] = result

        return self._todays_cache[key]


day_cache = _DayCache()
