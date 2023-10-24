import cv2
import json
with open('data/settings.json', 'r') as file:
    settings_data = json.load(file)
def resize_image(image, size):
    height, width = image.shape[:2]
    new_width, new_height = size
    otn = width / height
    if otn >= 1:
        if new_width < new_height:
            image = cv2.resize(image, (int(new_height * otn), new_height))
        else:
            image = cv2.resize(image, (new_width, int(new_width / otn)))
    else:
        if new_width > new_height:
            image = cv2.resize(image, (int(new_height * otn), new_height))
        else:
            image = cv2.resize(image, (new_width, int(new_width / otn)))
    return image