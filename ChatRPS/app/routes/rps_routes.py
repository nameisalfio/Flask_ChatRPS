from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.ml_models.rps_classifier import load_model, predict
import tempfile
import os

rps_bp = Blueprint('rps_bp', __name__)

# Load the RPS model
model_path = os.path.join(os.path.dirname(__file__), '..', 'ml_models', 'rps_model.pth')
rps_model = load_model(model_path)

@rps_bp.route('/classify', methods=['GET', 'POST'])
def rps_classify():
    prediction = None
    if request.method == 'POST':
        image = request.files.get('image')
        if image and image.filename:
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    image_path = os.path.join(temp_dir, secure_filename(image.filename))
                    image.save(image_path)

                    labels = {0: "rock", 1: "paper", 2: "scissors"}
                    prediction_index = predict(image_path, rps_model)
                    prediction = labels.get(prediction_index, "Unknown")
            except Exception as e:
                flash(f'Error processing image: {e}', 'error')
                return redirect(url_for('rps_bp.rps_classify'))
    
    return render_template('rps_classify.html', prediction=prediction)
