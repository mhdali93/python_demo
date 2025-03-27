from functools import wraps
import json
import time
from datetime import datetime
from flask import jsonify, request

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
        print(f"{current_time} :::: {message}")

    @staticmethod
    def profiling_dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            st_time = time.time()
            st_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            request_payload = request.get_json()
            
            result = func(*args, **kwargs)
            en_time = time.time()
            en_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            try:
                response_data = {
                    "request_time": st_dt,
                    "response_time": en_dt,
                    "execution_time": en_time - st_time,
                    "data": json.loads(result.get_data(as_text=True)) if result.get_data() else None
                }
                Utils.hi_print(f"{func.__name__}\nrequest_data: {request_payload}\nexecution_time: {en_time - st_time}\nresponse_data: {str(response_data)}")
                return jsonify(response_data)
            except Exception as e:
                Utils.hi_print(f"Error in profiling: {str(e)}")
                return result
        return wrapper


    