import functools
import time


def measure(func):
    @functools.wraps(func)
    def wrapper(*args, **kargs):
        start_time = time.time()

        result = func(*args, **kargs)

        execution_time = time.time() - start_time
        print('%.2f[ms] @%s' % (execution_time * 1000, func.__name__))
        return result

    return wrapper
