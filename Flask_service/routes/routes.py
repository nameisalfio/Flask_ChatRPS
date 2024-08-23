from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from Flask_service.routes.rps_classifier import load_model, predict
import tempfile
import os
import transformers
import torch

# Define blueprint
main_bp = Blueprint('main_bp', __name__)

# Set device to CUDA if available, else CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load models
base_dir = os.path.dirname(os.path.abspath(__file__))
rps_model = load_model(os.path.join(base_dir, '..', 'ml_models', 'rps_model.pth'))

# Load Llama 3 tokenizer and model
model_id = "meta-llama/Meta-Llama-3.1-8B"
pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    tokenizer=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device=device.index if device.type == 'cuda' else 'cpu', 
    max_new_tokens=50,  
    pad_token_id=128001  
)

@main_bp.route('/')
def index():
    return render_template('base.html')

@main_bp.route('/text-processing', methods=['GET', 'POST'])
def process_text():
    generated_text = None
    if request.method == 'POST':
        input_text = request.form.get('input_text', '').strip()
        if input_text:
            try:
                generated_text = pipeline(input_text)[0]['generated_text']
            except Exception as e:
                flash(f'Error processing text: {e}', 'error')
                return redirect(url_for('main_bp.process_text'))
    return render_template('text_processing.html', generated_text=generated_text)

@main_bp.route('/image-processing', methods=['GET', 'POST'])
def process_image():
    prediction = None
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
                    prediction = labels.get(label_index, "Unknown")

            except Exception as e:
                flash(f'Error processing image: {e}', 'error')
                return redirect(url_for('main_bp.process_image'))
    return render_template('image_processing.html', prediction=prediction)
