import json

CAPTCHA_DIR = 'captcha'
CRYPTED_EVENTID = "d4035a23e47b9aba13d9f64eae8aad9f"
TICKET_COUNT = 1
ENABLE_TICKET_AREA = True
CHAR_LIST = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

with open('captcha_substring.json', 'r') as f:
    CAPTCHA_SUBSTRING = json.load(f)
