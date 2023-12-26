from cnn_translate import CAPTCHA_Translater
import utils
import cv2

filename = 'yvyc.png'
img = cv2.imread(utils.get_img_path(filename))
translater = CAPTCHA_Translater()
print(translater.translate(img))
