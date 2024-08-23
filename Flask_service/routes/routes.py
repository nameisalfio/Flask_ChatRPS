from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from Flask_service.routes.rps_classifier import load_model, predict
import tempfile
import os
from huggingface_hub import InferenceClient
import torch

# Define the blueprint
main_bp = Blueprint('main_bp', __name__)

# Load the RPS model
rps_model = load_model(os.path.join(os.path.dirname(__file__), '..', 'ml_models', 'rps_model.pth'))

# Configure InferenceClient of Hugging Face for Llama 3
client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token="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"  
)

@main_bp.route('/')
def index():
    return render_template('base.html')

@main_bp.route('/text-processing', methods=['GET', 'POST'])
def process_text():
    session.setdefault('chat_history', [])

    if request.method == 'POST':
        input_text = request.form.get('input_text', '').strip()
        if input_text:
            try:
                session['chat_history'].append({'role': 'User', 'content': input_text})

                # Generate text using the Hugging Face API
                response = "".join(
                    message.choices[0].delta.content 
                    for message in client.chat_completion(
                        messages=[{"role": "user", "content": input_text}],
                        max_tokens=500,
                        stream=True,
                    )
                )

                session['chat_history'].append({'role': 'Bot', 'content': response})
            except Exception as e:
                flash(f'Error processing text: {e}', 'error')
                return redirect(url_for('main_bp.process_text'))

    return render_template('text_processing.html', chat_history=session['chat_history'])

@main_bp.route('/image-processing', methods=['GET', 'POST'])
def process_image():
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
