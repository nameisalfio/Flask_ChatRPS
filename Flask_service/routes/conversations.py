from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# Create a Blueprint for conversations
conversations_bp = Blueprint('conversations_bp', __name__)
mysql = MySQL()

@conversations_bp.route('/conversations')
def conversations_list():
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT c.id, c.user_id, c.prompt, c.response, c.timestamp, u.name
        FROM conversations c
        LEFT JOIN users u ON c.user_id = u.ID
    ''')
    conversations = cursor.fetchall()
    cursor.close()
    return render_template('conversations.html', conversations=conversations)

@conversations_bp.route('/conversations/create', methods=['GET', 'POST'])
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
                return redirect(url_for('conversations_bp.create_conversation'))
            
            cursor.execute('INSERT INTO conversations (user_id, prompt, response) VALUES (%s, %s, %s)', 
                           (user_id, prompt, response))
            mysql.connection.commit()
            flash('Conversation created successfully!', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error creating conversation: {e}', 'error')
        finally:
            cursor.close()

        return redirect(url_for('conversations_bp.conversations_list'))

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()

    return render_template('create_conversation.html', users=users)
