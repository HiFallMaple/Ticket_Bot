from PIL import Image
from tqdm import tqdm
import os
import re

for i in tqdm(range(100)):
	# 開啟PNG圖片
	image = Image.open(f'captcha/{i}.png')

	# 建立一個新的白色底圖
	new_image = Image.new("RGB", image.size, (255, 255, 255))

	# 將原始圖片貼到新的底圖上
	new_image.paste(image, (0, 0), mask=image)

	# 儲存修改後的圖片
	new_image.save(f'captcha_whitebg/{i}.png')