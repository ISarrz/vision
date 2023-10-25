import cv2

for i in range (1, 200):
    im = cv2.imread(f'data/screenshots/{i}.jpg')

    with open(f'data/screenshots/{i}.txt', 'r') as file:
        text = file.read()
    print(text)
    cv2.imshow('', im)
    cv2.waitKey(0)