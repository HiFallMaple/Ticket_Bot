from datetime import datetime
import json

CAPTCHA_DIR = 'captcha'
CRYPTED_EVENTID = "54fdee72c71c18cc2b694801e11e77cd"
TICKET_COUNT = 2
ENABLE_TICKET_AREA = True
CHAR_LIST = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
SCHEDULE_TIME = datetime(2023, 12, 29, 12, 00, 0)

with open('captcha_substring.json', 'r') as f:
    CAPTCHA_SUBSTRING = json.load(f)
