from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os
from Flask_service.routes.rps_classifier import load_model, predict
from flask_mysqldb import MySQL
import tempfile
import shutil

upload_image_bp = Blueprint('upload_image_bp', __name__)
mysql = MySQL()

# Load model at Blueprint initialization
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, '..', 'ml_models', 'rps_model.pth')

model = load_model(model_path)

@upload_image_bp.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No image uploaded', 'error')
            return redirect(url_for('upload_image_bp.upload_image'))

        image = request.files['image']
        if image.filename == '':
            flash('No selected file', 'error')
            return redirect(url_for('upload_image_bp.upload_image'))

        try:
            temp_dir = tempfile.mkdtemp() 
            image_path = os.path.join(temp_dir, secure_filename(image.filename))
            image.save(image_path)

            # Make prediction
            label_index = predict(image_path, model)
            labels = {0: "rock", 1: "paper", 2: "scissors"}
            prediction = labels.get(label_index, "Unknown")

            # Clean up: remove temporary directory and files
            shutil.rmtree(temp_dir)

            return render_template('result.html', prediction=prediction)

        except Exception as e:
            flash(f'Error processing image: {e}', 'error')
            return redirect(url_for('upload_image_bp.upload_image'))

    return render_template('upload_image.html')
