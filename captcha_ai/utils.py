from . import config

def get_img_path(filename):
	return f'{config.CAPTCHA_DIR}/{filename}'

def get_img_label(filename):
    return filename[:config.CAPTCHA_LEN]