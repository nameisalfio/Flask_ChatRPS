from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from Flask_service.routes.rps_classifier import load_model, predict
from flask_mysqldb import MySQL
import tempfile
import shutil 
import os

# Define blueprint and MySQL instance
main_bp = Blueprint('main_bp', __name__)
mysql = MySQL()

# Load model at Blueprint initialization
base_dir = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(base_dir, '..', 'ml_models', 'rps_model.pth'))

@main_bp.route('/')
def index():
    return render_template('base.html')

@main_bp.route('/rps_classify', methods=['GET', 'POST'])
def classify_image():
    if request.method == 'POST':
        image = request.files.get('image')

        if not image or image.filename == '':
            flash('No image selected', 'error')
            return redirect(url_for('main_bp.classify_image'))

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                image_path = os.path.join(temp_dir, secure_filename(image.filename))
                image.save(image_path)

                # Make prediction
                label_index = predict(image_path, model)
                labels = {0: "rock", 1: "paper", 2: "scissors"}
                prediction = labels.get(label_index, "Unknown")

                return render_template('upload_image.html', prediction=prediction)

        except Exception as e:
            flash(f'Error processing image: {e}', 'error')
            return redirect(url_for('main_bp.classify_image'))

    return render_template('upload_image.html')
