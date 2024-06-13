import inspect
from time import time


class Timer:
  def __init__(self, name):
    self.begin = 0
    self.name = name

  def start(self):
    self.begin = time()

  def stop(self):
    if not self.begin:
      raise f'timer was not started'
    stack = inspect.stack()
    caller_function = stack[1][0].f_code.co_name
    print(f'{self.name}.{caller_function} time: {time() - self.begin:.3f}s')
    self.begin = 0
