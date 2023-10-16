import json

from dataset import extract_letters
import cv2



if __name__ == "__main__":
    with open("encodes.json", 'r') as file:
        encodes = json.load(file)
    im = cv2.imread("text.jpg")
    letters = extract_letters(im)
