import shutil
from tqdm import tqdm

with open(f'captcha/tag', 'r') as f:
	lines = f.readlines()
	num_lines = len(lines)
	print(num_lines)
	for i, value in enumerate(lines):
		dst = f"captcha_ai/CAPTCHA/{value.strip()}.png"
		print(dst)
		content = shutil.copy2(f'captcha_whitebg/{i}.png', dst)
		
# with open(f'captcha/tag', 'a') as f:
# 	for i in range(num_lines, 100):
# 		content = shutil.copy2(f'captcha/{i}.svg', "output.svg")
# 		ans = input(f"Press Enter captcha of {i}.svg: ")
# 		f.write(ans + '\n')