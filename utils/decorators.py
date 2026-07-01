from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if current_user.role != role:
                flash('Access denied. Admins only.', 'danger')
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
