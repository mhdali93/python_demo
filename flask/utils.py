from functools import wraps
import json
import time
from datetime import datetime

class Utils:
    def __highlighted_print(func):
        def wrapper(*args, **kwargs):
            print(f"\n {'-'*100}")
            func(*args, **kwargs)
            print(f"{'-'*100} \n")
        return wrapper
    
    @staticmethod
    @__highlighted_print
    def hi_print(message):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time} -> {message}")

    @staticmethod
    def profiling_dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            st_time = time.time()
            st_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = func(*args, **kwargs)
            en_time = time.time()
            en_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            response_data = {
                "request_time": st_dt,
                "response_time": en_dt,
                "excecution_time": en_time - st_time,
                "data": json.loads(result.get_data(as_text=True))
            }
            Utils.hi_print(f"End time {func.__name__}, excecution time: {en_time - st_time}")
            return response_data
        return wrapper

    @staticmethod
    def logging_dec(func):
        def wrapper(*args, **kwargs):
            Utils.hi_print(f"{str(*args)},{str(**kwargs)}")
            result = func(*args,**kwargs)
            Utils.hi_print(str(result))
            return result
        return wrapper





    