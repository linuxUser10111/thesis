from flask import Flask, render_template, request, jsonify

import numpy as np
from PIL import Image
import pickle 
from project.ml_model import img_rows, img_cols, model_file_name, score_file_name, upload_model_and_score
import os.path

# test github action

app = Flask(__name__)

# hear starts the Rest API
# that can handel requests from frontend  and send back responses

def convertPictureToData(picture):
    img_resized = picture.resize((img_rows, img_cols))
    img_gray = img_resized.convert('L')
    image = np.asarray(img_gray)
    image = image.reshape(1,28,28,1)
    image = image / 255.0
    image = 1 - image
    return image


@app.get("/")
def root(): 
    if not os.path.exists(score_file_name) or not os.path.exists(model_file_name):
        print('retrain the model and upload files')
        upload_model_and_score()
    
    score = pickle.load(open("score.pkl", "rb"))
    return render_template('homepage.html', accuracy=score[1] * 100)
    

@app.route('/predict', methods=['POST'])
def prediction():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file part'})
    
    img = Image.open(file.stream)
    image = convertPictureToData(img)
    # print(image)
    model = pickle.load(open(model_file_name, "rb"))
    prediction= model.predict(image)
    
    print(prediction)
    
    predicted_value = np.argmax(prediction)
    probabelity = prediction.max() * 100
    
    if(probabelity <= 20):
        predicted_value = "the uplouded image is not a number"
    
    return render_template('prediction.html', prediction= predicted_value, probabelity=probabelity)

