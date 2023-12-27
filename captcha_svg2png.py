from PIL import Image
from tqdm import tqdm
import os
import re
import cairosvg
from config import CAPTCHA_DIR

files = os.listdir(CAPTCHA_DIR)
files = [file for file in files if re.match(r'.*\.svg', file)]

for file in tqdm(files):
    svg_path = os.path.join(CAPTCHA_DIR, file)
    png_path = os.path.join(CAPTCHA_DIR, file.replace('.svg', '.png'))
    cairosvg.svg2png(url=svg_path, write_to=png_path, scale=0.5)
    image = Image.open(png_path)
    new_image = Image.new("RGB", image.size, (255, 255, 255))
    new_image.paste(image, (0, 0), mask=image)
    new_image.save(png_path)