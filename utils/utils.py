from datetime import datetime, timedelta
from functools import wraps
from pprint import pp
from typing import Any, Callable, Dict, TypeVar, Tuple

R = TypeVar('R')

def get_current_time():
    return datetime.now()

def get_time_difference(start_time):
    return datetime.now() - start_time

def time_something(func: Callable[..., R]) -> Callable[..., Tuple[R, timedelta]]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Tuple[R, timedelta]:
        start_time = get_current_time()
        
        # Call the original function
        result = func(*args, **kwargs)
        
        time_diff = get_time_difference(start_time)
        
        return result, time_diff
    return wrapper

def pretty_print(data: Dict[Any, Any]) -> None:
    """
    Pretty prints any Python dictionary, list, or other data structure.
    
    Args:
        data (Any): The data structure to be pretty printed.
    """
    
    pp(data, indent=2)
