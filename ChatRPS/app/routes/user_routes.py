from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.user import User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to access your profile.', 'warning')
        return redirect(url_for('auth_bp.login_page'))
    
    user = User.query.get(user_id)
    if user is None:
        flash('User not found.', 'danger')
        return redirect(url_for('auth_bp.login_page'))

    return render_template('profile.html', user=user)

@user_bp.route('/update/<int:id>', methods=['POST'])
def update_user(id):
    user = User.query.get(id)
    if user is None:
        flash('User not found.', 'danger')
        return redirect(url_for('user_bp.profile'))

    user.name = request.form.get('name')
    user.lastname = request.form.get('lastname')
    user.username = request.form.get('username')
    user.email = request.form.get('email')
    password = request.form.get('password')
    if password:
        user.password = password

    db.session.commit()
    flash('User updated successfully!', 'success')
    return redirect(url_for('user_bp.profile'))

@user_bp.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        flash('User not found.', 'danger')
        return redirect(url_for('user_bp.profile'))

    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    session.pop('user_id', None)
    return redirect(url_for('auth_bp.login_page'))
