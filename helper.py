import errno
import json
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.misc
from scipy.ndimage import rotate
from scipy.stats import bernoulli
import itertools
import json
import os
import h5py
import random

# Some useful constants
DRIVING_LOG_FILE = './data/driving_log.csv'
IMG_PATH = './data/'
STEERING_COEFFICIENT = 0.229
input_shape = (27, 107, 3)
NO_IMAGES = 3


def load_image(line, j):
    img = plt.imread("data/" + (line[j]).strip())
    img = crop(img)
    return img
    # random_gamma(img)


def load_normalize_image(line, j):
    image = load_image(line, j)
    image_list = image.flatten().tolist()
    image_array = np.reshape(np.array(image_list), newshape=input_shape)
    image_array = image_array / 255 - 0.5
    return image_array


def crop(image):
    return image[65:145:3, 0:-1:3, :]


def random_flip(image, steering_angle):
    head = random.choice(range(0, 1))
    if head:
        return np.fliplr(image), -1 * steering_angle
    else:
        return image, steering_angle


def random_gamma(image):
    """
    Random gamma correction is used as an alternative method changing the brightness of
    training images.
    http://www.pyimagesearch.com/2015/10/05/opencv-gamma-correction/
    :param image:
        Source image
    :return:
        New image generated by applying gamma correction to the source image
    """
    gamma = np.random.uniform(0.4, 1.5)
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


def pltTrainingData(data):
    plt.figure(figsize=(16, 8))
    for c in range(10):
        index = random.randint(0, len(data))
        plt.subplot(4, 4, c + 1)
        plt.axis('off')
        img = np.array(load_image(data[index], 0))
        img = np.squeeze(img)
        plt.imshow(img)


def pltSteeringAnglrHistrogram(steering_angle):
    plt.figure()
    plt.hist(steering_angle, bins=51)
    plt.title("Histogram of Steering Angle")
    plt.show()


def pltflipped(data):
    plt.figure(figsize=(16, 8))
    plt.title("Flipped Images")
    plt.subplot(2, 2, 1)
    plt.axis('off')
    img = np.array(load_image(data[0], 0))
    img = np.squeeze(img)
    plt.imshow(img)
    img = np.fliplr(img)
    plt.subplot(2, 2, 2)
    plt.axis('off')
    plt.imshow(img)


def get_images(drivingLogRow):
    X_train = []
    y_train = []
    ### load all images
    for j in range(3):
        image = np.array(load_normalize_image(drivingLogRow, j), )
        # center camera image
        if j == 0:
            steering_angle = float(drivingLogRow[3])
        # left camera image
        elif j == 1:
            steering_angle = float(drivingLogRow[3]) + STEERING_COEFFICIENT
        # right camera image
        elif j == 2:
            steering_angle = float(drivingLogRow[3]) - STEERING_COEFFICIENT

        image, steering_angle = random_flip(image, steering_angle)

        # image = random_gamma(image)

        X_train.append(image.tolist())
        y_train.append(steering_angle)
    assert len(X_train) == len(y_train), 'len(X_train) == len(y_train) should be same'
    return np.array(X_train), np.array(y_train)



def generator(drivingLogRows, batch_size=64):
    infiniteDrivingLogRows = itertools.cycle(drivingLogRows)
    counter = 0
    X = []
    y = []
    while True:
        if (counter >= batch_size):
            counter = 0
            X_x = np.array(X).reshape(NO_IMAGES * len(X), 27, 107, 3)
            y_y = np.array(y).reshape(NO_IMAGES * len(y))
            X = []
            y = []
            yield X_x, y_y
        drivingLogRow = next(infiniteDrivingLogRows)
        features, labels = get_images(np.squeeze(drivingLogRow))
        X.append(features.tolist())
        y.append(labels.tolist())
        counter = counter + NO_IMAGES


def save_model(model):
    # Save the model.
    # If the model.json file already exists in the local file,
    # warn the user to make sure if user wants to overwrite the model.
    if 'model.json' in os.listdir():
        os.remove('model.json')
    if 'model.h5' in os.listdir():
        os.remove('model.h5')
    else:
        # Save model as json file
        json_string = model.to_json()

        with open('model.json', 'w') as outfile:
            json.dump(json_string, outfile)

            # save weights
            model.save_weights('./model.h5')
            print("Saved")



