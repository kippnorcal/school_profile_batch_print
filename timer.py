import time
import logging


def _timer_message(func, elapsed, value):
    """Private function for formatting log message so the correct
    unit is displayed based on the elapsed seconds.

    Args:
        func: the function called in the wrapper
        elapsed: float of elapsed seconds

    Returns:
        String message for logging.
    """
    unit = "seconds"
    if elapsed >= 60:
        elapsed = round(elapsed / 60, 2)
        unit = "minutes"

    return f"{func.__name__} completed {value} in {elapsed} {unit}."


def _calc_elapsed(end, start):
    """Private function for formatting elapsed time between two
    timestamps. Should be provided from time.time() in standard
    library.

    Args:
        end: time as float
        start: time as float

    Returns:
        A float rounded to 2 decimal places.
    """
    elapsed = round(end - start, 2)
    return elapsed


def elapsed(func):
    """Decorator function used to compute and report the time a
    function takes to complete. Add to a function as: @elapsed"""

    def wrapper(*args):
        start = time.time()
        value = func(*args)
        end = time.time()
        elapsed = _calc_elapsed(end, start)
        logging.info(_timer_message(func, elapsed, value))

    return wrapper
