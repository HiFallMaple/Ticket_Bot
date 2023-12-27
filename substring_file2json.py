import json
from config import CHAR_LIST


captcha_substring = dict()

for ch in CHAR_LIST:
    for i in range(4):
        if ch not in captcha_substring:
            captcha_substring[ch] = [-99, -99, -99, -99]
        with open(f'captcha_substring/{ch}_{i}', 'r') as f:
            captcha_substring[ch][i] = f.read().replace(
                "\" /></svg>", "").strip()[10:-10]

with open('captcha_substring.json', 'w') as f:
    json.dump(captcha_substring, f)
