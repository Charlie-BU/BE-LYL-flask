from functools import wraps
from flask import g, redirect, url_for, jsonify


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return jsonify({
                "status": 401,
                'message': "未登录！"
            })
    return inner