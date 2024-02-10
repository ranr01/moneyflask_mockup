import functools

from flask import (
    Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for, abort,
)
from werkzeug.security import check_password_hash


def auth_bp_factory(
        get_user_from_db_by_username,
        get_user_from_db_by_user_id,
        post_login_route,
        post_logout_route,
    ):
    bp = Blueprint('auth', __name__, url_prefix='/auth')


    @bp.route('/login', methods=('GET', 'POST'))
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            error = None
            user = get_user_from_db_by_username(username)

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for(post_login_route))

            flash(error)

        return render_template('auth/login.html')

    @bp.before_app_request
    def load_logged_in_user():
        user_id = session.get('user_id')

        if user_id is None:
            g.user = None
        else:
            g.user = get_user_from_db_by_user_id(user_id)

    @bp.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for(post_logout_route))

    return bp


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def role_required(role):
    def wrapper(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user['role'] != role:
                abort(403)

            return view(**kwargs)

        return wrapped_view
    
    return wrapper




