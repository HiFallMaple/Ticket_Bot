
import copy
import itertools
from tqdm import tqdm
import concurrent.futures
from config import CHAR_LIST

CAPTCHA_LIST: list
with open(f'captcha/tag', 'r') as f:
    CAPTCHA_LIST = [i.strip() for i in f.readlines()]
 
def find_ch_in_captcha(ch, index):
    result = []
    for i, l in enumerate(CAPTCHA_LIST):
        if l[index] == ch:
            result.append((i, l))
    return result

def get_max_same_string(str1, str2):
    if str1 is not None and str2 is not None:
        max_string = str1 if len(str1) >= len(str2) else str2
        min_string = str1 if len(str1) < len(str2) else str2
        length = len(min_string)
        while length > 0:
            for start in range(len(min_string) - length + 1):
                sub_string = min_string[start:start+length]
                if sub_string in max_string:
                    return sub_string
            length -= 1
    return ""

def count_same_characters(str1, str2):
    return sum(a == b for a, b in zip(str1, str2))

def check_and_remove(lst):
    for tuple1, tuple2 in itertools.combinations(lst, 2):
        str1 = tuple1[1]
        str2 = tuple2[1]
        if count_same_characters(str1, str2) > 1:
            lst.remove(tuple1)
            return False
    return True

def find_substring_of_ch(captcha_list, ch, i):
    while True:
        if check_and_remove(captcha_list):
            break
    with open(f'captcha/{captcha_list[0][0]}.svg', 'r') as f:
        str1 = f.read().strip()[137:]
    with open(f'captcha/{captcha_list[1][0]}.svg', 'r') as f:
        str2 = f.read().strip()[137:]
    sub_string = get_max_same_string(str1, str2)
    with open(f'captcha_substring/{ch}_{i}', 'w') as f:
        f.write(sub_string)

def count_same_characters(str1, str2):
    return sum(a == b for a, b in zip(str1, str2))

THREAD_NUM = 12
char_position = dict()

print(CAPTCHA_LIST)

for ch in CHAR_LIST:
    for i in range(4):
        if ch not in char_position:
            char_position[ch] = [-99,-99,-99,-99]
        char_position[ch][i] = find_ch_in_captcha(ch, i)
        
print(char_position)

with tqdm(total=len(CHAR_LIST)*4) as pbar:
        # let's give it some more threads:
        with concurrent.futures.ProcessPoolExecutor(max_workers=THREAD_NUM) as executor:
            futures = list()
            for ch in CHAR_LIST:
                for i in range(4):
                    futures.append(executor.submit(find_substring_of_ch, copy.deepcopy(char_position[ch][i]), ch, i))
            for future in concurrent.futures.as_completed(futures):

                pbar.update(1)
