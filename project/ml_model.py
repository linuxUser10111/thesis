from keras import layers
from keras.datasets import mnist
from keras import Sequential
from keras.callbacks import EarlyStopping
from keras.utils import to_categorical
from keras.losses import categorical_crossentropy
from keras import backend as K

import joblib



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

joblib.dump(model, 'mnist_model.pkl')