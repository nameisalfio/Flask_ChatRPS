from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# Create a Blueprint for users
users_bp = Blueprint('users_bp', __name__)
mysql = MySQL()

@users_bp.route('/users')
def users_list():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    return render_template('users.html', users=users)

@users_bp.route('/users/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        try:
            cursor.execute('INSERT INTO users (name, lastname, username, email, password) VALUES (%s, %s, %s, %s, %s)', 
                           (name, lastname, username, email, password))
            mysql.connection.commit()
            flash('User created successfully!', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error creating user: {e}', 'error')
        finally:
            cursor.close()

        return redirect(url_for('users_bp.users_list'))

    return render_template('create_user.html')
