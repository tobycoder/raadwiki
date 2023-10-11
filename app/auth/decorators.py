from functools import wraps
from flask import g, request, redirect, url_for, session, flash
from firebase_admin import auth
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if('user' not in session):
            return redirect(url_for('auth.rw_login_user', next=request.url))
        elif('user' in session):
            user = auth.get_user_by_email(session['user'])
            if user.disabled == True:
                session.pop('user')
                flash('Je account is gedeactiveerd door een beheerder.')
                return redirect(url_for('auth.rw_login_user', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def master_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if('user' in session):
            if(session['user'] != 'floris@florisdeboer.com'):
                flash('Je moet beheerder zijn om hier te komen.')
                return redirect(url_for('auth.rw_login_user', next=request.url))
        else:
            flash('Je moet ingelogd zijn om hier te komen.')
            return redirect(url_for('auth.rw_login_user', next=request.url))
        return f(*args, **kwargs)
    return decorated_function