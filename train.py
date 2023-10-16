import idx2numpy
import numpy as np
import cv2

emnist_path = 'C:/Users/German/Documents/code/proj/emnist/'
X_train = idx2numpy.convert_from_file(emnist_path + 'emnist-balanced-train-images-idx3-ubyte')
y_train = idx2numpy.convert_from_file(emnist_path + 'emnist-balanced-train-labels-idx1-ubyte')

X_test = idx2numpy.convert_from_file(emnist_path + 'emnist-balanced-test-images-idx3-ubyte')
y_test = idx2numpy.convert_from_file(emnist_path + 'emnist-balanced-test-labels-idx1-ubyte')

X_train = np.reshape(X_train, (X_train.shape[0], 28, 28, 1))
X_test = np.reshape(X_test, (X_test.shape[0], 28, 28, 1))

n = 4
im = X_train[n]
im = cv2.resize(im, (28 * 10, 28 * 10), interpolation=cv2.INTER_LINEAR)
im = cv2.rotate(im, cv2)

cv2.imshow("", im)
cv2.waitKey(0)