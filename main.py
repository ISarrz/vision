import json
import keras
import numpy as np
import cv2
from math import sqrt

import numpy as np
import time
from flask import Flask, render_template, Response

import imutils
from imutils import contours

with open("encodes.json", 'r') as file:
    encodes = json.load(file)
model = keras.models.load_model('emnist_letters.h5')

camera = cv2.VideoCapture('2.mp4')
green = (50, 255, 0)


def convert_image(im):
    image = im.copy()

    grey = ~cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])  # contrast
    grey = cv2.filter2D(grey, -1, kernel)

    grey = cv2.medianBlur(grey, 5)
    grey = cv2.GaussianBlur(grey, (5, 5), 0)
    grey = cv2.GaussianBlur(grey, (13, 13), 0)

    # calculate thresh borders
    v = np.median(image)
    sigma = 0.33
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))

    ret, thresh_img = cv2.threshold(grey, lower, upper, cv2.THRESH_BINARY)

    return thresh_img


def find_contours(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if not contours:
        print('no')
        return []

    diagonals = []
    for ind, contour in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(contour)
        diagonal = sqrt(w ** 2 + h ** 2)
        diagonals.append(diagonal)
    diagonals.sort()
    sr_diagonal = sum(diagonals[1:-2]) / len(diagonals[1:-2])
    max_diagonal = diagonals[-1]
    min_diagonal = diagonals[0]
    ex_contours = []
    for ind, contour in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(contour)
        diagonal = sqrt(w ** 2 + h ** 2)

        if diagonal >= sr_diagonal * 0.8 and diagonal <= max_diagonal * 0.5 and hierarchy[0][ind][3] == -1:
            ex_contours.append(contour)
    return ex_contours


def recognize(image, contour):
    (x, y, w, h) = cv2.boundingRect(contour)
    cropped = image[y:y + h, x:x + w]
    size_max = int(max(w, h) * 1.4)

    # moving to center
    letter_square = 255 * np.ones(shape=[size_max, size_max], dtype=np.uint8)
    x_0 = (size_max - w) // 2
    y_0 = (size_max - h) // 2
    letter_square[y_0:y_0 + h, x_0:x_0 + w] = cropped

    # reshaping for recognition
    letter_square = cv2.resize(letter_square, (28, 28), interpolation=cv2.INTER_AREA)
    letter_square = cv2.flip(letter_square, 1)
    letter_square = cv2.rotate(letter_square, cv2.ROTATE_90_COUNTERCLOCKWISE)
    letter_square = 1 - letter_square / 255

    # recognize
    predict = model.predict([letter_square])
    result = np.argmax(predict, axis=1)
    text = chr(encodes[str(result[0])])
    return text


def generate_frames():
    start_time = time.time()
    while True:
        success, frame = camera.read()
        if cv2.waitKey(1) & 0xFF == ord('q') or not success:
            break

        thresh_img = convert_image(frame)
        contours = find_contours(thresh_img)

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(thresh_img, (x, y), (x + w, y + h), (255, 255, 255), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), green, 2)

        cv2.imshow('', frame)

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    generate_frames()
