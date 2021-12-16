def handle_exceptions(internal_exception_cls, *exception_types_caught):

    def func_decorator(func):
        def argument_decorator(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_types_caught as e:
                raise internal_exception_cls(f'{type(e)} raised in {func.__name__} method')
        return argument_decorator
    return func_decorator
