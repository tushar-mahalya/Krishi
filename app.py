from flask import Flask, request
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
    return "Hello, I am alive"


@app.route("/detect-disease", methods=["POST"])
def detect_disease():
    plant_type = request.form["plant_type"]
    file = request.files["file"]
    
    # Check if plant type is valid
    model = get_model(plant_type)
    if model is None:
        return {"error": "Invalid plant type"}

    # Load image into PIL Image object
    image = Image.open(BytesIO(file.read()))

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

    # Return the predicted class and confidence score
    return {"plant_type": plant_type, "predicted_class": predicted_class, "confidence_score": confidence_score}
