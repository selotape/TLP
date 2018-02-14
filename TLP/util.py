import wrapt as wrapt


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def with_entry_log(log_meth):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        log_meth(f'== calling {wrapped.__name__}')
        return wrapped(*args, **kwargs)

    return wrapper
