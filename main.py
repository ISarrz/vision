import json
import keras
import numpy as np
import cv2
from math import sqrt
import cv2
import numpy as np
import time
from flask import Flask, render_template, Response
import cv2
import imutils
from imutils import contours

with open("encodes.json", 'r') as file:
    encodes = json.load(file)
model = keras.models.load_model('emnist_letters.h5')

camera = cv2.VideoCapture(0)
green = (50, 255, 0)







def generate_frames():
    start_time = time.time()
    while True:
        success, frame = camera.read()
        thresh = 140

        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(8, 8))

        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
        l, a, b = cv2.split(lab)  # split on 3 different channels

        l2 = clahe.apply(l)  # apply CLAHE to the L-channel

        lab = cv2.merge((l2, a, b))  # merge channels
        frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR


        grey = ~cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ret, thresh_img = cv2.threshold(grey, thresh, 250, cv2.THRESH_BINARY)
        output = thresh_img.copy()

        cnts, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        #img_contours = np.zeros(frame.shape)
        #cv2.drawContours(img_contours, contours, -1, (255, 255, 255), 1)
        #cv2.imshow("", img_contours)
        letters = []

        for ind, contour in enumerate(cnts):
            (x, y, w, h) = cv2.boundingRect(contour)
            diag = sqrt(w ** 2 + h ** 2)
            # if hierarchy[0][ind][3] == 0 and diag >= sr_diag:
            #if hierarchy[0][ind][3] == 0:

            if diag >= 100 and diag < 300 and hierarchy[0][ind][3] == -1:
                print(hierarchy[0][ind][3])
                croped = output[y:y + h, x:x + w]
                size_max = int(max(w, h) * 1.4)
                letter_square = 255 * np.ones(shape=[size_max, size_max], dtype=np.uint8)

                # центрируем
                x_0 = (size_max - w) // 2
                y_0 = (size_max - h) // 2
                letter_square[y_0:y_0 + h, x_0:x_0 + w] = croped
                letter_square = cv2.resize(letter_square, (28, 28), interpolation=cv2.INTER_AREA)

                letter_square = cv2.flip(letter_square, 1)
                letter_square = cv2.rotate(letter_square, cv2.ROTATE_90_COUNTERCLOCKWISE)
                letter_square = 1 - letter_square / 255
                # cv2.imshow("", letter_square)
                # cv2.waitKey(0)
                #letters.append([(x, y, w, h), letter_square])
                cv2.rectangle(output, (x, y), (x + w, y + h), (70, 0, 0), 1)
        cv2.imshow('', output)
        if cv2.waitKey(1) & 0xFF == ord('q') or not success:
            break



    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    generate_frames()
