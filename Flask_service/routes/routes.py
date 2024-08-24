from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from Flask_service.routes.rps_classifier import load_model, predict
import tempfile
import os
from flask_mysqldb import MySQL
import datetime
from huggingface_hub import InferenceClient

# Define the blueprint
main_bp = Blueprint('main_bp', __name__)

# Load the RPS model
rps_model = load_model(os.path.join(os.path.dirname(__file__), '..', 'ml_models', 'rps_model.pth'))

# Configure InferenceClient of Hugging Face for Llama 3
client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token="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"  
)

# Initialize MySQL
mysql = MySQL()

@main_bp.route('/')
def index():
    """
    Input: None
    Function: Renders the base HTML template, serving as the homepage.
    Output: HTML page (base.html)
    """
    return render_template('base.html')


@main_bp.route('/conversations')
def list_conversations():
    """
    Input: None (GET request)
    Function: Retrieves a list of conversations from the database and passes it to the template.
    Output: HTML page displaying the list of conversations.
    """
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT c.id, c.start_time, u.username FROM conversations c JOIN users u ON c.user_id = u.ID")
        conversations = cursor.fetchall()  # Fetches all results from the query
    except Exception as e:
        flash(f'Error fetching conversations: {e}', 'error')
        conversations = []
    finally:
        cursor.close()
    
    return render_template('list_conversations.html', conversations=conversations)


@main_bp.route('/new-conversation', methods=['GET', 'POST'])
def create_conversation():
    """
    Input: 
        - GET request: None (renders form).
        - POST request: User ID from the form data.
    Function: 
        - GET: Renders a form for creating a new conversation.
        - POST: Inserts a new conversation into the database for the selected user.
    Output: 
        - GET: HTML page with the form to create a conversation.
        - POST: Redirects to the conversation detail page if successful, or displays an error message.
    """
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        if user_id:
            try:
                cursor = mysql.connection.cursor()
                cursor.execute("INSERT INTO conversations (user_id) VALUES (%s)", (user_id,))
                mysql.connection.commit()
                conversation_id = cursor.lastrowid
                flash('Conversation created successfully!', 'success')
                return redirect(url_for('main_bp.view_and_update_conversation', conversation_id=conversation_id))
            except Exception as e:
                mysql.connection.rollback()
                flash(f'Error creating conversation: {e}', 'error')
            finally:
                cursor.close()
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT ID, username FROM users")
        users = cursor.fetchall()
    except Exception as e:
        flash(f'Error fetching users: {e}', 'error')
        users = []
    finally:
        cursor.close()

    return render_template('create_conversation.html', users=users)


@main_bp.route('/conversation/<int:conversation_id>', methods=['GET', 'POST'])
def view_and_update_conversation(conversation_id):
    """
    Input: 
        - GET request: Conversation ID from the URL.
        - POST request: User's input text from the form.
    Function: 
        - GET: Fetches conversation details and messages from the database.
        - POST: Adds a new message to the conversation using the user's input and AI-generated response.
    Output: 
        - GET: HTML page displaying the conversation details and messages.
        - POST: HTML page refreshed with the new message added.
    """
    if request.method == 'POST':
        input_text = request.form.get('input_text', '').strip()
        if input_text:
            try:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Generate response using the Hugging Face API
                response = "".join(
                    message.choices[0].delta.content 
                    for message in client.chat_completion(
                        messages=[{"role": "user", "content": input_text}],
                        max_tokens=2048,
                        stream=True,
                    )
                )

                # Add user message to the database
                cursor = mysql.connection.cursor()
                cursor.execute("""
                    INSERT INTO messages (conversation_id, prompt, response, timestamp)
                    VALUES (%s, %s, %s, %s)
                """, (conversation_id, input_text, response, timestamp))
                mysql.connection.commit()

                flash('Message added successfully!', 'success')

            except Exception as e:
                mysql.connection.rollback()
                flash(f'Error processing text: {e}', 'error')
                return redirect(url_for('main_bp.view_and_update_conversation', conversation_id=conversation_id))
            finally:
                cursor.close()

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT * FROM messages WHERE conversation_id = %s ORDER BY timestamp
        """, (conversation_id,))
        messages = cursor.fetchall()

        cursor.execute("""
            SELECT * FROM conversations WHERE id = %s
        """, (conversation_id,))
        conversation = cursor.fetchone()
    except Exception as e:
        flash(f'Error fetching conversation: {e}', 'error')
        messages = []
        conversation = None
    finally:
        cursor.close()

    return render_template('view_and_update_conversation.html', conversation=conversation, messages=messages)


@main_bp.route('/image-processing', methods=['GET', 'POST'])
def process_image():
    """
    Input: 
        - GET request: None (renders the form).
        - POST request: Image file uploaded by the user.
    Function: 
        - GET: Renders a form for image upload.
        - POST: Processes the uploaded image and classifies it using the RPS model.
    Output: 
        - GET: HTML page with the form to upload an image.
        - POST: HTML page with the classification result displayed.
    """
    prediction = None
    if request.method == 'POST':
        image = request.files.get('image')
        if image and image.filename:
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    image_path = os.path.join(temp_dir, secure_filename(image.filename))
                    image.save(image_path)

                    # Make prediction
                    labels = {0: "rock", 1: "paper", 2: "scissors"}
                    prediction = labels.get(predict(image_path, rps_model), "Unknown")

            except Exception as e:
                flash(f'Error processing image: {e}', 'error')
                return redirect(url_for('main_bp.process_image'))
    
    return render_template('image_processing.html', prediction=prediction)
