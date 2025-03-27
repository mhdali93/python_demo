class Utils:
    def __add_identifiers(func):
        def wrapper(*args, **kwargs):
            print("--------------------------------**--------------------------------")
            func(*args, **kwargs)
            print("--------------------------------**--------------------------------")
        return wrapper
    
    @staticmethod
    @__add_identifiers
    def heavy_print(st):
        print(st)