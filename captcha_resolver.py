from config import CAPTCHA_SUBSTRING


def solve_captcha(svg: str):
    result = [0, 0, 0, 0]
    for key in CAPTCHA_SUBSTRING:
        for i in range(4):
            if CAPTCHA_SUBSTRING[key][i] in svg:
                result[i] = key
    return ''.join(result)
