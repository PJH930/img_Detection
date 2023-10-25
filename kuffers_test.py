from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
import os
import numpy as np
import cv2
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf

def make_test_date(filename):
    path = "./TestAll/"

    X = []
    Y = []

    full_path = path + filename
    print(full_path)
    img = cv2.imread(full_path)
    data = cv2.resize(img, (224, 224))
    X.append(data / 255.)
    Y.append(filename)

    # np array 형태로 변경
    X = np.array(X)
    Y = np.array(Y)

    return X, Y

print_msg = []


def test_one_sample(filename, model):
    global print_msg
    model = tf.keras.models.load_model(model)
    X, Y = make_test_date(os.path.basename(filename))
    for i, img in enumerate(X):
        input_x = np.expand_dims(img, axis=0)
        result = model.predict(input_x)
        ans = result[0].argmax()


        filename_split = Y[0].split("_")[3]
        print_msg.clear()
        if ans == 1:

            print("My ans is pass")
            print_msg.append("Model     : pass")
        elif ans == 0:
            print("My ans is fail")
            print_msg.append("Model     : fail")

        if filename_split == "pass":
            print("Pass")
            print_msg.append("filename : pass")
        elif filename_split == "fail":
            print("Pail")
            print_msg.append("filename : fail")

        key = cv2.waitKey(0)
        if key == 27:
            cv2.destroyAllWindows()
            exit(0)
