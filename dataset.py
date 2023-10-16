import json
import idx2numpy
from matplotlib import pyplot as plt
import numpy as np
import cv2
from math import sqrt


def extract_letters(img):
    letters = []
    im = cv2.imread(img)

    ##  filterd_image = cv2.medianBlur(my_photo, 3)
    filterd_image = cv2.GaussianBlur(im, (5, 5), 0)
    filterd_image = cv2.fastNlMeansDenoising(filterd_image, None, 20, 7, 21)
    img_grey = cv2.cvtColor(filterd_image, cv2.COLOR_BGR2GRAY)

    thresh = 140

    # get threshold image
    ret, thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)

    # output = thresh_img.copy()
    # find contours
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    sr_diag = 0

    for ind, contour in enumerate(contours[1:]):
        if hierarchy[0][ind][3] == 0:
            (x, y, w, h) = cv2.boundingRect(contour)
            sr_diag += sqrt(w ** 2 + h ** 2)

    sr_diag //= (len(contours[1:]))

    for ind, contour in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(contour)
        diag = sqrt(w ** 2 + h ** 2)
        if hierarchy[0][ind][3] == 0 and diag >= sr_diag:
            croped = thresh_img[y:y + h, x:x + w]
            size_max = int(max(w, h) * 1.1)
            letter_square = 255 * np.ones(shape=[size_max, size_max], dtype=np.uint8)

            # центрируем
            x_0 = (size_max - w) // 2
            y_0 = (size_max - h) // 2
            letter_square[y_0:y_0 + h, x_0:x_0 + w] = croped
            letter_square = cv2.resize(letter_square, (28 * 10, 28 * 10), interpolation=cv2.INTER_AREA)
            letter_square = ~letter_square
            letter_square = cv2.flip(letter_square, 1)
            letter_square = cv2.rotate(letter_square, cv2.ROTATE_90_COUNTERCLOCKWISE)
            letters.append(letter_square)
            # cv2.rectangle(output, (x, y), (x + w, y + h), (70, 0, 0), 1)

    return letters


if __name__ == "__main__":
    letters = extract_letters("text.jpg")
    for i in letters:
        cv2.imshow("", i)
        cv2.waitKey(0)
