import cv2
import numpy as np
from PIL import Image
import warnings
from tensorflow.keras.models import load_model
from keras.preprocessing.image import img_to_array

warnings.filterwarnings('ignore')

class IdentifyCaptcha:
    def __init__(self) -> None:
        self.info = {0: '2',1: '3',2: '4',3: '5',4: '6',5: '7',6: '8',7: 'b',8: 'c',9: 'd',10: 'e',11: 'f',12: 'g',13: 'm',14: 'n',15: 'p',16: 'w',17: 'x',18: 'y'}

    def from_pretrained(self, path):
        self.model = load_model(path, compile = False)
        return self
 
    def __preidict(self, num):
        img_arr = Image.fromarray(num)
        img_arr = img_to_array(img_arr)
        return img_arr
    
    def predict(self, img_path):
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 145, 0)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, np.ones((5, 2), np.uint8))
        img = cv2.dilate(img, np.ones((2, 2), np.uint8), iterations=1)
        img = cv2.GaussianBlur(img, (1, 1), 0)
        
        image_list = [img[10:50, 30:50], img[10:50, 50:70], img[10:50, 70:90], img[10:50, 90:110], img[10:50, 110:130]]
        
        x_inputs = [self.__preidict(x) for x in image_list]
        x_inputs = np.array(x_inputs)
        x_inputs /= 255.0

        y_predicts = self.model.predict(x_inputs, verbose=0)
        y_predicts = np.argmax(y_predicts, axis=1)
        captcha_ans = [self.info[x] for x in y_predicts]
        return ''.join(captcha_ans)
    
model = IdentifyCaptcha().from_pretrained('./model/result_model.h5')

if __name__ == "__main__":
    img_path = "samples/img50.png"
    model.predict(img_path)