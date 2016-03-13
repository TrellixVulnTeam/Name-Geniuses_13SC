from threading import Thread
from functools import wraps

from flask import redirect, url_for
from flask.ext.login import current_user


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            return redirect(url_for('unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
    
def check_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.admin is True:
            return func(*args, **kwargs)
        return redirect(url_for('dashboard'))
    return decorated_function