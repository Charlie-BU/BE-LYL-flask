from functools import wraps

# flask上下文装饰器
def with_app_context(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from app import app
        with app.app_context():
            return func(*args, **kwargs)

    return wrapper
