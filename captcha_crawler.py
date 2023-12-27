import os
from time import sleep, time

import cv2
import cairosvg
from PIL import Image

from captcha_resolver import solve_captcha
from captcha_ai import CAPTCHA_Translater
from crawler import login, get_products, get_captcha
from config import CAPTCHA_DIR


login()
products = get_products()
product = products["products"][0]
crypted_sessionId = product["sessionId"]


translater = CAPTCHA_Translater()
total = 0
correct = 0

while True:
    captcha_key, captcha_svg = get_captcha(crypted_sessionId, True)
    start_time = time()
    captcha = solve_captcha(captcha_svg)
    end_time = time()
    substring_cost = end_time - start_time

    png_path = "output.png"
    start_time = time()
    cairosvg.svg2png(bytestring=captcha_svg.encode(
        'utf8'), write_to=png_path, scale=0.5)
    image = Image.open(png_path)
    new_image = Image.new("RGB", image.size, (255, 255, 255))
    new_image.paste(image, (0, 0), mask=image)
    new_image.save(png_path)
    img = cv2.imread(png_path)
    cnn_captcha = translater.translate(img)
    end_time = time()
    cnn_cost = end_time - start_time
    if captcha == cnn_captcha:
        correct += 1
    total += 1
    print(captcha, cnn_captcha, captcha == cnn_captcha,
          correct / total, substring_cost, cnn_cost)

    # print(captcha)
    with open(os.path.join(CAPTCHA_DIR, f"{captcha}.svg"), 'w') as f:
        f.write(captcha_svg)
    sleep(1)
