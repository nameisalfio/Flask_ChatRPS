from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from Flask_service.routes.rps_classifier import load_model, predict
from flask_mysqldb import MySQL
import tempfile
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import os

# Define blueprint and MySQL instance
main_bp = Blueprint('main_bp', __name__)
mysql = MySQL()

# Autenticazione con Hugging Face
login(token="...")

# Load rsp classifier model
base_dir = os.path.dirname(os.path.abspath(__file__))
rps_model_path = os.path.join(base_dir, '..', 'ml_models', 'rps_model.pth')
rps_model = load_model(rps_model_path)

# Load LLaMA 3 tokenizer and model
llama_model_id = "meta-llama/Llama-3-13B"  # Replace with the actual model ID for LLaMA 3
tokenizer = AutoTokenizer.from_pretrained(llama_model_id)
llama_model = AutoModelForCausalLM.from_pretrained(llama_model_id)

@main_bp.route('/')
def index():
    return render_template('base.html')

@main_bp.route('/text_processing', methods=['GET', 'POST'])
def text_processing():
    text_result = None

    if request.method == 'POST':
        input_text = request.form.get('input_text', '').strip()
        if input_text:
            try:
                inputs = tokenizer(input_text, return_tensors='pt')
                outputs = llama_model.generate(**inputs)
                text_result = tokenizer.decode(outputs[0], skip_special_tokens=True)
            except Exception as e:
                flash(f'Error processing text: {e}', 'error')
                return redirect(url_for('main_bp.text_processing'))

    return render_template('text_input.html', text_result=text_result)

@main_bp.route('/image_processing', methods=['GET', 'POST'])
def image_processing():
    image_result = None

    if request.method == 'POST':
        image = request.files.get('image')
        if image and image.filename != '':
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    image_path = os.path.join(temp_dir, secure_filename(image.filename))
                    image.save(image_path)

                    # Make prediction
                    label_index = predict(image_path, rps_model)
                    labels = {0: "rock", 1: "paper", 2: "scissors"}
                    image_result = labels.get(label_index, "Unknown")

            except Exception as e:
                flash(f'Error processing image: {e}', 'error')
                return redirect(url_for('main_bp.image_processing'))

    return render_template('image_input.html', image_result=image_result)
