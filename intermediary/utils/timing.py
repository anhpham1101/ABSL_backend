from time import time

def timming(func):
    def calculateTime(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(f'API {func.__name__!r} executed in {(end-start):.4f}s')
        return result
    return calculateTime
    