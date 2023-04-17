from flask import Flask, render_template
from flask import jsonify, request
from PIL import Image
import numpy as np
import json
from io import BytesIO
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Loading information of saved models and training dataset
with open('/home/studio-lab-user/Krishi/artifacts/dataset_info.json') as f:
    dataset_info = json.load(f)
    
with open('/home/studio-lab-user/Krishi/artifacts/model_info.json') as f:
    model_info = json.load(f)


def get_model(plant_type: str):
    if plant_type not in model_info.keys():
        return None
    model_path = model_info[plant_type]['Saved Path']
    model = load_model(model_path)
    return model


@app.route("/")
def ping():
    return render_template('index.html')


@app.route("/detect_disease", methods=["POST", "GET"])
def detect_disease():
    if request.method == 'POST':
        plant_type = request.form["plant-type"]
        file = request.files["plant-image"]
    
    # Check if plant type is valid
    model = get_model(plant_type)
    if model is None:
        return {"error": "Invalid plant type"}

    # Load image into PIL Image object
    image = Image.open(BytesIO(file.read())).resize((256,256))
    
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image.save('static/temp_img/temp_img.png', format = 'PNG')
    
    # Convert image to array
    image_arr = np.array(image)
    
    # Convert image to single batch
    image_batch = np.expand_dims(image_arr, 0)

    # Make prediction using the appropriate model
    prediction = model.predict(image_batch)

    # Get predicted class and confidence score
    class_index = np.argmax(prediction[0])
    predicted_class = dataset_info[plant_type]['classes'][class_index]
    confidence_score = float(np.max(prediction[0]))

    
    return render_template('index.html', plant_tp = plant_type, detected_d = predicted_class, confi_scr = f"{confidence_score*100:.2f} %")

if __name__ == '__main__':
    app.run(debug = True)
