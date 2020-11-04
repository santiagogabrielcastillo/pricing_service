import functools
from typing import Callable
from flask import session, flash, redirect, url_for, current_app


def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_func(*args, **kwargs):
        if not session.get('email'):
            flash('You need to be signed in for this page', 'danger')
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)
    return decorated_func  # importante que no lleve paréntesis al final (queremos la función y no su ejecución)


def requires_admin(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get('email') != current_app.config.get('ADMIN', ''):  # si no hay admin, str vacío como default
            flash('You need to be an admin to access this page', 'danger')
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)
    return decorated_func