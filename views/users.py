from flask import Blueprint, request, render_template, url_for, session, redirect, flash
from models.user import User, UserErrors


users_bp = Blueprint('users', __name__)


@users_bp.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            User.register_user(email, password)
            session['email'] = email
            return redirect(url_for('alerts.index'))
        except UserErrors.UserError as e:
            return e.message
    return render_template('users/register.html')


@users_bp.route('/login', methods=['GET', 'POST'])
def login_user():
    if session['email']:
        flash('You are logged in!')
        return redirect(url_for('alerts.index'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            User.is_login_valid(email, password)
            session['email'] = email
            return redirect(url_for('alerts.index'))
        except UserErrors.UserError as e:
            return e.message
    return render_template('users/login.html')


@users_bp.route('/logout')
def logout():
    session['email'] = None
    return redirect(url_for('home'))
