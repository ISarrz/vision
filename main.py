import json
import keras

import cv2
from math import sqrt

import numpy as np
import time


class Object:
    def __init__(self, x, y, w, h, time_update, symbol=""):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center_x = x + w // 2
        self.center_y = y + h // 2
        self.diagonal = sqrt(w ** 2 + h ** 2)
        self.symbol = symbol
        self.time_update = time_update
        self.time_recognize = time_update

    def check(self, x, y, w, h):
        center_x = x + w // 2
        center_y = y + h // 2
        delta_x = abs(center_x - self.center_x)
        delta_y = abs(center_y - self.center_y)
        delta_diagonal = sqrt(delta_x ** 2 + delta_y ** 2)
        if abs(delta_diagonal <= self.diagonal / 2):
            return True
        return False

    def update(self, x, y, w, h, time_update):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center_x = x + w // 2
        self.center_y = y + h // 2
        self.diagonal = sqrt(w ** 2 + h ** 2)
        #self.symbol = symbol
        self.time_update = time_update


class Application:
    def __init__(self, video_input='3.mp4'):
        self.video = cv2.VideoCapture(video_input)
        self.objects = []
        with open("encodes.json", 'r') as file:
            self.encodes = json.load(file)
        self.model = keras.models.load_model('emnist_letters.h5')
        self.GREEN = (0, 255, 0)
        self.WHITE = (255, 255, 255)

    def convert_image(self, im):
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

    def find_contours(self, image):
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

    def recognize(self, image, contour):
        (x, y, w, h) = cv2.boundingRect(contour)
        cropped = image[y:y + h, x:x + w]
        size_max = int(max(w, h) * 1.4)

        # moving to center
        letter_square = 255 * np.zeros(shape=[size_max, size_max], dtype=np.uint8)
        x_0 = (size_max - w) // 2
        y_0 = (size_max - h) // 2
        letter_square[y_0:y_0 + h, x_0:x_0 + w] = cropped

        # reshaping for recognition
        letter_square = cv2.resize(letter_square, (28, 28), interpolation=cv2.INTER_AREA)
        letter_square = cv2.flip(letter_square, 1)
        letter_square = cv2.rotate(letter_square, cv2.ROTATE_90_COUNTERCLOCKWISE)
        letter_square = np.expand_dims(letter_square, axis=0)
        letter_square = letter_square / 255

        # return "x"
        # recognize
        predict = self.model.predict([letter_square])
        result = np.argmax(predict, axis=1)
        text = chr(self.encodes[str(result[0])])
        return text

    def generate_frames(self, refresh_time):
        start_time = time.time()
        while True:
            success, frame = self.video.read()
            if cv2.waitKey(1) & 0xFF == ord('q') or not success:
                break

            thresh_img = self.convert_image(frame)
            contours = self.find_contours(thresh_img)
            refreshed_objects = []
            for object in self.objects:
                if time.time() - object.time_update < 5:
                    refreshed_objects.append(object)
            self.objects = refreshed_objects
            for contour in contours:
                find = False
                (x, y, w, h) = cv2.boundingRect(contour)
                for object in self.objects:
                    if object.check(x, y, w, h):
                        find = True
                        if time.time() - object.time_recognize > 2:
                            object.symbol = self.recognize(thresh_img, contour)
                            object.time_recognize = time.time()
                        object.update(x, y, w, h, time.time())
                        cv2.rectangle(frame, (x, y), (x + w, y + h), self.GREEN, 2)
                        frame = cv2.putText(frame, object.symbol, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, self.GREEN, 3, cv2.LINE_AA)
                        break

                if not find:
                    object = Object(x, y, w, h, time.time(), self.recognize(thresh_img, contour))
                    self.objects.append(object)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), self.GREEN, 2)
                    frame = cv2.putText(frame, 'X', (x, y), cv2.FONT_HERSHEY_SIMPLEX , 2, self.GREEN, 3, cv2.LINE_AA)

            cv2.imshow('', frame)

        self.video.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    a = Application()
    a.generate_frames(0.2)
