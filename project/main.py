from flask import Flask, render_template, request, jsonify

import numpy as np
from PIL import Image


from keras import layers
from keras.datasets import mnist
from keras import Sequential
from keras.callbacks import EarlyStopping
from keras.utils import to_categorical
from keras.losses import categorical_crossentropy
from keras import backend as K



# input image dimensions
img_rows, img_cols = 28, 28
# number of channels
num_channels = 1
# number of classes
num_classes = 10

def train_test_split():
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    input_shape = None
    
    if K.image_data_format() == 'channels_first':
        X_train = X_train.reshape(X_train.shape[0], num_channels, img_rows, img_cols)
        X_test = X_test.reshape(X_test.shape[0], num_channels, img_rows, img_cols)
        input_shape = (num_channels, img_rows, img_cols)
    else:
        X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, num_channels)
        X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, num_channels)
        input_shape = (img_rows, img_cols, num_channels)
    
    return X_train, X_test, y_train, y_test, input_shape


def get_early_stopping():
    return EarlyStopping(min_delta=1,patience=5, restore_best_weights=True)



def fit_model(X_train, X_valid, y_train, y_valid, early_stopping, input_shape):
    
   model = Sequential([
    layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape),
    layers.Conv2D(64, (3, 3), activation='relu'),    
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Dropout(0.25),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(num_classes, activation='softmax')
    ])
   
   model.compile(
        loss=categorical_crossentropy, optimizer='adam', metrics=['accuracy']
    )
   model.fit(
        X_train, y_train,
        validation_data=(X_valid, y_valid),
        batch_size=512,
        epochs=50,
        callbacks=[early_stopping]
    )
   return model



# train the model and calculate accurecy before starting server 
X_train, X_test, y_train, y_test, input_shape = train_test_split()
    
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
    
y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)
    
early_stopping = get_early_stopping()
    
model = fit_model(X_train=X_train, X_valid=X_test, y_train=y_train, y_valid=y_test, early_stopping=early_stopping, input_shape=input_shape)
score = model.evaluate(X_test, y_test)


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
    
    prediction= model.predict(image)
    
    print(prediction)
    
    predicted_value = np.argmax(prediction)
    probabelity = prediction.max() * 100
    
    if(probabelity <= 20):
        predicted_value = "the uplouded image is not a number"
    
    return render_template('prediction.html', prediction= predicted_value, probabelity=probabelity)


if __name__ == "__main__": 
    app.run(host="127.0.0.1", port=8080, debug=True)

# how to convert a picture into data for our neural network?