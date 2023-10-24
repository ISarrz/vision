import json
import keras
import cv2
from math import sqrt
import numpy as np
import time
from functions import *


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
        # self.symbol = symbol
        self.time_update = time_update


class Application:
    def __init__(self):
        with open('data/settings.json', 'r') as file:
            settings_data = json.load(file)
        if settings_data['video_input_type'] == 'file':
            self.video = cv2.VideoCapture(settings_data['video_file_name'])
        else:
            self.video = cv2.VideoCapture(int(settings_data['video_input_name']))
        self.objects = []
        with open("data/encodes.json", 'r') as file:
            self.encodes = json.load(file)
        self.model = keras.models.load_model('data/emnist_letters.h5')
        self.GREEN = (0, 255, 0)
        self.WHITE = (255, 255, 255)

    def convert_image(self, im):
        image = im.copy()

        gray = ~cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])  # contrast
        gray = cv2.filter2D(gray, -1, kernel)

        gray = cv2.medianBlur(gray, 5)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        # gray = cv2.GaussianBlur(gray, (13, 13), 0)

        ret, thresh_img = cv2.threshold(gray, 128, 192, cv2.THRESH_OTSU)
        thresh_img = cv2.GaussianBlur(thresh_img, (5, 5), 0)

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
        if len(diagonals[1:-2]) == 0:
            print('no')
            return []
        # contours.sort(key=lambda x:sqrt(cv2.boundingRect(x)[2] ** 2 + cv2.boundingRect(x)[3] ** 2))
        # if len(contours) > 30:
        #     contours = contours[:30]
        sr_diagonal = sum(diagonals[1:-2]) / len(diagonals[1:-2])
        max_diagonal = diagonals[-1]
        min_diagonal = diagonals[0]
        ex_contours = []
        for ind, contour in enumerate(contours):
            (x, y, w, h) = cv2.boundingRect(contour)
            diagonal = sqrt(w ** 2 + h ** 2)

            if diagonal >= sr_diagonal * 0.9 and diagonal <= max_diagonal * 0.5 and hierarchy[0][ind][3] == -1:
                ex_contours.append(contour)
        return ex_contours

    def convert_to_string(self):
        strings = {}
        answer = ''
        self.objects.sort(key=lambda x: [x.x, x.y])
        medium_width = 0
        medium_height = 0
        for i in self.objects:
            medium_width += i.w
            medium_height += i.h
        medium_width /= len(self.objects)
        medium_height /= len(self.objects)
        x_0, y_0 = self.objects[0].x, min(self.objects, key=lambda x: x.y).y
        for i in self.objects:
            number = (i.y - y_0) // medium_height
            if strings.get(number):
                strings[number].append(i)
            else:
                strings[number] = [i]
        for key in strings.keys():
            answer += strings[key][0].symbol
            for i in range(len(strings[key]) - 1):
                if strings[key][i + 1].x - (strings[key][i].x + strings[key][i].w) >= medium_width / 2:
                    answer += ' ' + strings[key][i + 1].symbol
                else:
                    answer += strings[key][i + 1].symbol
            answer += '\n'
        return answer

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

    def generate_frames(self, e):
        with open('data/settings.json', 'r') as file:
            settings_data = json.load(file)
        if e.control.selected:
            while True and e.control.selected:
                if 's' in e.control.content.controls[0].value:
                    try:
                        e.control.content.controls[0].value = e.control.content.controls[0].value.replace('s', '')
                        cv2.imwrite('screenshot.jpg', frame)
                    except Exception:
                        e.control.content.controls[0].value = e.control.content.controls[0].value.replace('s', '')
                if 'c' in e.control.content.controls[0].value:
                    try:
                        e.control.content.controls[1].value = self.convert_to_string()
                        e.control.content.controls[0].value = e.control.content.controls[0].value.replace('c', '')
                    except Exception:
                        e.control.content.controls[0].value = e.control.content.controls[0].value.replace('c', '')
                        pass
                if 'p' in e.control.content.controls[0].value:
                    continue
                success, frame = self.video.read()
                if cv2.waitKey(1) & 0xFF == ord('q') or not success:
                    break

                thresh_img = self.convert_image(frame)
                output = frame.copy()
                contours = self.find_contours(thresh_img)
                refreshed_objects = []
                for object in self.objects:
                    if time.time() - object.time_update < 1:
                        refreshed_objects.append(object)
                self.objects = refreshed_objects
                for contour in contours:
                    find = False
                    (x, y, w, h) = cv2.boundingRect(contour)
                    for object in self.objects:
                        if object.check(x, y, w, h):
                            find = True
                            if time.time() - object.time_recognize > 1:
                                object.symbol = self.recognize(thresh_img, contour)
                                object.time_recognize = time.time()
                            object.update(x, y, w, h, time.time())
                            cv2.rectangle(output, (x, y), (x + w, y + h), self.GREEN, 2)
                            output = cv2.putText(output, object.symbol, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, self.GREEN,
                                                 3,
                                                 cv2.LINE_AA)
                            break

                    if not find:
                        object = Object(x, y, w, h, time.time(), self.recognize(thresh_img, contour))
                        self.objects.append(object)
                        cv2.rectangle(output, (x, y), (x + w, y + h), self.GREEN, 2)
                        output = cv2.putText(output, 'X', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, self.GREEN, 3,
                                             cv2.LINE_AA)

                if settings_data['video_type'] == 'normal':
                    width = int(settings_data['video_window_size'][0])
                    height = int(settings_data['video_window_size'][1])
                    output = resize_image(output, (width, height))
                    cv2.imshow('', output)
                else:
                    output = thresh_img
                    width = int(settings_data['video_window_size'][0])
                    height = int(settings_data['video_window_size'][1])
                    output = resize_image(output, (width, height))
                    cv2.imshow('', output)

                cv2.waitKey(1)

            self.video.release()
            cv2.destroyAllWindows()
            e.control.selected = False
            e.control.update()
        else:
            e.control.selected = False
            e.control.update()


a = Application()

if __name__ == "__main__":
    a = Application()
    a.generate_frames()
