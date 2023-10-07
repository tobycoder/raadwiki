from functools import wraps
from flask import g, request, redirect, url_for, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if('user' not in session):
            return redirect(url_for('auth.rw_login_user', next=request.url))
        return f(*args, **kwargs)
    return decorated_function