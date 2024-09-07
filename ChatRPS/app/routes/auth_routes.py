from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from app.models.user import User
from app import db
from datetime import datetime

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/', methods=['GET'])
def home():
    if 'user_id' in session:
        return redirect(url_for('user_bp.profile'))
    return redirect(url_for('auth_bp.login_page'))

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
        flash('Invalid username or password', 'error')
    
    if 'user_id' in session:
        return redirect(url_for('user_bp.profile'))
    
    return render_template('login.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('auth_bp.login_page'))

@auth_bp.route('/login_page', methods=['GET'])
def login_page():
    if 'user_id' in session:
        return redirect(url_for('user_bp.profile'))
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match. Please try again.')
            return redirect(url_for('auth_bp.register'))

        if User.query.filter_by(username=username).first():
            flash('This username is already taken. Please choose another one.')
            return redirect(url_for('auth_bp.register'))

        if User.query.filter_by(email=email).first():
            flash('This email is already taken. Please use another email.')
            return redirect(url_for('auth_bp.register'))

        user = User(name=name, lastname=lastname, username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! You can now log in.')
        return redirect(url_for('auth_bp.login'))

    return render_template('register.html')