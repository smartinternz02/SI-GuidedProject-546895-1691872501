import numpy as np
from flask import Blueprint, Flask, render_template, request, jsonify
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model
app = Flask(__name__)
IMG_HEIGHT, IMG_WIDTH = 150, 150
model1 = load_model("C:\\Users\\vigne\\OneDrive\\Desktop\\vignesh\\vd\\vdmaincode\\chest_xray_classification_model.h5")
pneumonia_prediction_bp = Blueprint('pneumonia_prediction', __name__)
@pneumonia_prediction_bp.route('/predict_pneumonia', methods=['POST'])
def predict_pneumonia():
    user_file = request.files.get('file')
    if not user_file:
        return jsonify({'prediction': 'Error: No file uploaded'})
    try:
        image_path = "C:\\Users\\vigne\\OneDrive\\Desktop\\vignesh\\vd\\templates\\temp_image.png"
        user_file.save(image_path)
        new_image = load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
        new_image = img_to_array(new_image)
        new_image = new_image / 255.0
        new_image = np.expand_dims(new_image, 0)
        prediction = model1.predict(new_image)
        predicted_class = 'Pneumonia' if prediction[0] > 0.5 else 'Normal'
        return jsonify({'prediction': predicted_class})
    except Exception as e:
        print("Error during pneumonia prediction:", str(e))
        return jsonify({'prediction': 'Error during pneumonia prediction'})
@app.route('/make_appointment')
def make_appointment():
    return render_template('appointment.html')
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'xray_image_file' in request.files:
            user_xray_image = request.files['xray_image_file']
            if user_xray_image:
                image_path = "C:\\Users\\vigne\\OneDrive\\Desktop\\vignesh\\vd\\templates\\temp_image.png"
                user_xray_image.save(image_path)
                new_image = load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
                new_image = img_to_array(new_image)
                new_image = new_image / 255.0
                new_image = np.expand_dims(new_image, 0)
                prediction = model1.predict(new_image)
                predicted_class = 'Pneumonia' if prediction[0] > 0.5 else 'Normal'
                response = {'prediction': predicted_class}
                return jsonify(response)
        return render_template('pneumonia1.html')
app.register_blueprint(pneumonia_prediction_bp)
if __name__ == '__main__':
    app.run(debug=True)