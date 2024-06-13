from functools import wraps
from time import time


def time_on_call(func):
  @wraps(func)
  def wrapper(*args, **kw):
    begin = time()
    print(f'called {func.__name__}')
    try:
      res = func(*args, **kw)
    finally:
      print(f'finished {func.__name__} in {time() - begin:.3f}s')
    return res

  return wrapper
