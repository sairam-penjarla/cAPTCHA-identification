import os
from flask import Flask, redirect, jsonify, request, url_for, render_template, flash
from PIL import Image
from tensorflow.keras.models import load_model
import numpy as np
from keras.preprocessing.image import img_to_array
import cv2
app = Flask(__name__)
model = load_model('/Users/sai/Desktop/everything/Programming/cAPTCHA/result_model.h5', compile = False)
path = "/Users/sai/Desktop/everything/Programming/cAPTCHA/samples/"
def get_demo(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 145, 0)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, np.ones((5, 2), np.uint8))
    img = cv2.dilate(img, np.ones((2, 2), np.uint8), iterations=1)
    img = cv2.GaussianBlur(img, (1, 1), 0)
    image_list = [img[10:50, 30:50], img[10:50, 50:70], img[10:50, 70:90], img[10:50, 90:110], img[10:50, 110:130]]
    Xdemo = []
    for i in range(5):
        Xdemo.append(img_to_array(Image.fromarray(image_list[i])))

    Xdemo = np.array(Xdemo)
    Xdemo /= 255.0

    ydemo = model.predict(Xdemo)
    ydemo = np.argmax(ydemo, axis=1)
    captcha_ans = []
    info = {0: '2',1: '3',2: '4',3: '5',4: '6',5: '7',6: '8',7: 'b',8: 'c',9: 'd',10: 'e',11: 'f',12: 'g',13: 'm',14: 'n',15: 'p',16: 'w',17: 'x',18: 'y'}
    for res in ydemo:
        captcha_ans.append(info[res])
    return (''.join(captcha_ans))

@app.route("/")
def home():
    return render_template("upload_image.html")


# Route to upload image
@app.route('/upload-image', methods=['POST'])
def upload_image():
    cAPTCHA_data = [0]
    image = request.files["cAPTCHA_image"]
    image.save(os.path.join(path, image.filename))
    predicted_captcha = get_demo('/Users/sai/Desktop/everything/Programming/cAPTCHA/samples/' + str(image.filename))
    cAPTCHA = {'file_name': image.filename,'captcha_text': predicted_captcha}
    cAPTCHA_data[0] = cAPTCHA
    return render_template("upload_image.html", cAPTCHA_data=cAPTCHA_data)


@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    from flask import send_from_directory
    return send_from_directory(path, filename)

if __name__ == "__main__":
    app.run()