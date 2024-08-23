from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os
from rps_classifier import load_model, predict
from flask_mysqldb import MySQL

# Initialize Blueprint
main_bp = Blueprint('main', __name__)

# Initialize MySQL connection
mysql = MySQL()

# Load model at Blueprint initialization
model_path = os.path.join('ml_models', 'rps_model.pth')
model = load_model(model_path)

@main_bp.route('/')
def index():
    return render_template('base.html')

@main_bp.route('/users')
def users():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    return render_template('users.html', users=users)

@main_bp.route('/conversations')
def conversations():
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT c.id, c.user_id, c.prompt, c.response, c.timestamp, u.name
        FROM conversations c
        LEFT JOIN users u ON c.user_id = u.ID
    ''')
    conversations = cursor.fetchall()
    cursor.close()
    return render_template('conversations.html', conversations=conversations)

@main_bp.route('/create_user', methods=['GET', 'POST'])
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

        return redirect(url_for('main.users'))

    return render_template('create_user.html')

@main_bp.route('/create_conversation', methods=['GET', 'POST'])
def create_conversation():
    if request.method == 'POST':
        user_id = request.form['user_id']
        prompt = request.form['prompt']
        response = request.form['response']

        cursor = mysql.connection.cursor()
        try:
            cursor.execute('SELECT * FROM users WHERE ID = %s', (user_id,))
            user = cursor.fetchone()
            if not user:
                flash('User does not exist', 'error')
                return redirect(url_for('main.create_conversation'))
            
            cursor.execute('INSERT INTO conversations (user_id, prompt, response) VALUES (%s, %s, %s)', 
                           (user_id, prompt, response))
            mysql.connection.commit()
            flash('Conversation created successfully!', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error creating conversation: {e}', 'error')
        finally:
            cursor.close()

        return redirect(url_for('main.conversations'))

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()

    return render_template('create_conversation.html', users=users)

@main_bp.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No image uploaded', 'error')
            return redirect(url_for('main.upload_image'))

        image = request.files['image']
        if image.filename == '':
            flash('No selected file', 'error')
            return redirect(url_for('main.upload_image'))

        # Use current_app to access the app's config
        temp_folder = current_app.config['TEMP_FOLDER']
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)

        image_path = os.path.join(temp_folder, secure_filename(image.filename))
        image.save(image_path)
        
        label_index = predict(image_path, model)
        labels = {0: "rock", 1: "paper", 2: "scissors"}
        prediction = labels.get(label_index, "Unknown")

        return render_template('result.html', prediction=prediction)

    return render_template('upload_image.html')
