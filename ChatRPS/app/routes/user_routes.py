from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ChatRPS.app import db
from ChatRPS.app.models.user import User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/profile', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to access your profile.', 'warning')
        return redirect(url_for('auth_bp.login_page'))
    
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('auth_bp.login_page'))

    return render_template('profile.html', user=user)

@user_bp.route('/update', methods=['GET'])
def update_form():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to update your profile.', 'warning')
        return redirect(url_for('auth_bp.login_page'))
    
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('user_bp.profile'))

    return render_template('update_form.html', user=user)

@user_bp.route('/update', methods=['POST'])
def update_user():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to update your profile.', 'warning')
        return redirect(url_for('auth_bp.login_page'))
    
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('user_bp.profile'))

    # Get form data
    name = request.form.get('name')
    lastname = request.form.get('lastname')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Update only non-null values
    if name:
        user.name = name
    if lastname:
        user.lastname = lastname
    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.password = password
    
    try:
        db.session.commit()
        flash('Profile updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {e}', 'danger')
    
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
