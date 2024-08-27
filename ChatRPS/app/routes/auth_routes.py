from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('user_bp.profile'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth_bp.login_page'))

    return render_template('index.html')

@auth_bp.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        flash('You have been logged out', 'success')
    return redirect(url_for('auth_bp.login_page'))

@auth_bp.route('/')
def login_page():
    return render_template('index.html')
