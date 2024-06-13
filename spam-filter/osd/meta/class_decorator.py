def decorate_all_functions(function_decorator):
  def decorator(cls):
    for name, obj in vars(cls).items():
      if callable(obj):
        try:
          obj = obj.__func__  # unwrap Python 2 unbound method
        except AttributeError:
          pass  # not needed in Python 3
        setattr(cls, name, function_decorator(obj))
    return cls

  return decorator
