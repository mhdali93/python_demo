import time
from datetime import datetime

class Utils:
    def __highlighted_print(func):
        def wrapper(*args, **kwargs):
            print(f"\n {'%'*200} \n")
            func(*args, **kwargs)
            print(f"\n {'$'*200} \n")
        return wrapper
    
    @__highlighted_print
    @staticmethod
    def hi_print(message):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time} -> {message}")

    @staticmethod
    def profiling_dec(func):
        def wrapper(*args, **kwargs):
            Utils.hi_print(f"Start time {func.__name__}")
            func(*args, **kwargs)
            Utils.hi_print(f"End time {func.__name__}")
        return wrapper







    