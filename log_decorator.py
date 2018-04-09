from functools import wraps

class LogDecorator:
    def __init__(self, file_name):
        self.file = open(file_name)
    
    def __call__(self, func):
        @wraps(func)
        def decorated(*args, kwargs):
            ret = func(*args, **kwargs)
            self.file.write('{}\n'.format(ret))
            return ret
        return decorated
    
    def close(self):
        self.file.close()
