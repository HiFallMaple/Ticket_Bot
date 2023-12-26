import shutil
from time import sleep
from crawler import login, get_products, get_captcha
import cairosvg
from PIL import Image
from tqdm import tqdm

import os
import re

def find_max_number_in_captcha_dir(directory):
    max_number = -1
    pattern = re.compile(r'(\d+)\.png$')
    if not os.path.exists(directory):
        return max_number
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            number = int(match.group(1))
            if number > max_number:
                max_number = number
    return max_number

# 使用函數並打印結果
captcha_dir = 'captcha'
max_number = find_max_number_in_captcha_dir(captcha_dir)

login()
products = get_products()
product = products["products"][0]
crypted_sessionId = product["sessionId"]
for i in tqdm(range(max_number + 1, 100)):
    captcha_key = get_captcha(crypted_sessionId, True)
    cairosvg.svg2png(url="output.svg", write_to=f"{captcha_dir}/{i}.png", scale=5)
    shutil.copy2("output.svg", f"{captcha_dir}/{i}.svg")
    sleep(1)
