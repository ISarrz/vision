import json
import keras
from dataset import extract_letters
import cv2
import numpy as np

if __name__ == "__main__":
    with open("encodes.json", 'r') as file:
        encodes = json.load(file)
    model = keras.models.load_model('emnist_letters.h5')
    letters = extract_letters("text.jpg")
    for i in letters:
        img_arr = np.expand_dims(i, axis=0)
        #img_arr = img_arr / 255.0

        #img_arr = img_arr.reshape((1, 28, 28, 1))
        predict = model.predict([img_arr])
        result = np.argmax(predict, axis=1)
        print(chr(encodes[str(result[0])]))
        cv2.imshow("", i)
        cv2.waitKey(0)
