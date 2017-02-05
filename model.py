from keras.layers import Conv2D, Flatten
from keras.layers.core import Dropout
from keras.layers.pooling import MaxPooling2D
from keras.models import Sequential
from keras.layers import Dense, Input, Activation
from keras.optimizers import SGD, Adam, RMSprop

N_CLASSES = 1 # The output is a single digit: a steering angle

BATCH_SIZE = 64 # The lower the better
EPOCHS = 5 # The higher the better
LEARNING_RATE = 0.0015

import helper

# read all image files from a directory. later on batching needs to be supported
# from data directory
import csv
import random


img_dir = "data/"
label_dir = "{}/driving_log.csv".format(img_dir)
input_shape = (27, 107, 3)

# import img_label
data = []

with open(label_dir) as file:
    reader = csv.reader(file)
    for i in reader:
        data.append(i)

print("imported data")
data_size = len(data)
print("size of import data", data_size)
print("visualize import data: ", data[random.randrange(data_size)])

random.shuffle(data)
train_data = data[:int(data_size*.8)]
validate_data = data[int(data_size*.8):int(data_size*.9)]
test_data = data[int(data_size*.9):]

print("train size:", len(train_data))
print("valid size:", len(validate_data))
print("test size:", len(test_data))

no_samples_per_epoch = len(train_data)*3
validation_samples = len(validate_data)*3
test_samples = len(test_data)*3

# number of convolutional filters to use
nb_filters1 = 16
nb_filters2 = 8
nb_filters3 = 4
nb_filters4 = 2

# size of pooling area for max pooling
pool_size = (2, 2)

# convolution kernel size
kernel_size = (3, 3)

# Initiating the model
model = Sequential()

# Starting with the convolutional layer
# The first layer will turn 1 channel into 16 channels
model.add(Conv2D(nb_filters1, kernel_size[0], kernel_size[1],
                        border_mode='valid',
                        input_shape=input_shape))
# Applying ReLU
model.add(Activation('relu'))
# The second conv layer will convert 16 channels into 8 channels
model.add(Conv2D(nb_filters2, kernel_size[0], kernel_size[1]))
# Applying ReLU
model.add(Activation('relu'))
# The second conv layer will convert 8 channels into 4 channels
model.add(Conv2D(nb_filters3, kernel_size[0], kernel_size[1]))
# Applying ReLU
model.add(Activation('relu'))
# The second conv layer will convert 4 channels into 2 channels
model.add(Conv2D(nb_filters4, kernel_size[0], kernel_size[1]))
# Applying ReLU
model.add(Activation('relu'))
# Apply Max Pooling for each 2 x 2 pixels
model.add(MaxPooling2D(pool_size=pool_size))
# Apply dropout of 25%
model.add(Dropout(0.25))

# Flatten the matrix. The input has size of 360
model.add(Flatten())
# Input 360 Output 16
model.add(Dense(16))
# Applying ReLU
model.add(Activation('relu'))
# Input 16 Output 16
model.add(Dense(16))
# Applying ReLU
model.add(Activation('relu'))
# Input 16 Output 16
model.add(Dense(16))
# Applying ReLU
model.add(Activation('relu'))
# Apply dropout of 50%
model.add(Dropout(0.5))
# Input 16 Output 1
model.add(Dense(N_CLASSES))

model.summary()



model.compile(loss='mean_squared_error',
              optimizer=Adam(LEARNING_RATE),
              metrics=['accuracy'])


# 6. create three generators for training, validation and testing
train_gen = helper.generator(train_data, batch_size=64)
validation_gen = helper.generator(validate_data, batch_size=64)
test_gen = helper.generator(test_data, batch_size=64)


##  7. Train Model

history = model.fit_generator(train_gen, 
                    nb_epoch=EPOCHS,
                    samples_per_epoch=no_samples_per_epoch,
                    nb_val_samples=validation_samples,
                    validation_data=validation_gen,
                    verbose=1)

helper.save_model(model)
score = model.evaluate_generator(test_gen, test_samples)
print('Test score:', score[0])
print('Test accuracy:', score[1])