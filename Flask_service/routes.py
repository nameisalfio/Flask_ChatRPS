from flask import Flask, render_template, request, redirect, url_for, flash
from app import app, mysql

@app.route('/')
def index():
    return render_template('base.html')

# Route per visualizzare la lista degli utenti
@app.route('/users')
def users():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    return render_template('users.html', users=users)

# Route per visualizzare la lista delle conversazioni
@app.route('/conversations')
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

# Route per creare un nuovo utente
@app.route('/create_user', methods=['GET', 'POST'])
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
        except:
            mysql.connection.rollback()
            flash('Error creating user. Make sure all fields are filled and username/email are unique.', 'error')
        finally:
            cursor.close()

        return redirect(url_for('users'))

    return render_template('create_user.html')

# Route per visualizzare il modulo di creazione della conversazione
@app.route('/create_conversation', methods=['GET', 'POST'])
def create_conversation():
    if request.method == 'POST':
        user_id = request.form['user_id']
        prompt = request.form['prompt']
        response = request.form['response']

        cursor = mysql.connection.cursor()
        try:
            # Verifica se l'utente esiste
            cursor.execute('SELECT * FROM users WHERE ID = %s', (user_id,))
            user = cursor.fetchone()
            if not user:
                flash('User does not exist', 'error')
                return redirect(url_for('create_conversation'))
            
            cursor.execute('INSERT INTO conversations (user_id, prompt, response) VALUES (%s, %s, %s)', 
                           (user_id, prompt, response))
            mysql.connection.commit()
            flash('Conversation created successfully!', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error creating conversation: {e}', 'error')
        finally:
            cursor.close()

        return redirect(url_for('conversations'))

    # Se è una richiesta GET, recupera gli utenti per popolare il menu a discesa
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()

    return render_template('create_conversation.html', users=users)
