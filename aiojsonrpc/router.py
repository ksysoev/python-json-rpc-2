from .exceptions import MethodNotFound

class Router():
    _methods = {}

    @classmethod
    def method(cls, method):
        """Decorator for adding new method to Router"""
        if method.__name__ in cls._methods:
            raise ValueError('Dublicate Method Name')
        
        cls._methods[method.__name__] = method

        return method
    
    @classmethod
    def dispatch(cls, request):
        if request.method not in cls._methods:
            raise MethodNotFound(f"Method {request.method} isn't found")

        return cls._methods[request.method]

    @classmethod
    def clear(cls):
        cls._methods.clear()

        





        