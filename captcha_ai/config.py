import logging
import os
from torchvision import transforms

logging.basicConfig(level=logging.INFO)

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
current_dir: str = os.path.dirname(os.path.realpath(__file__))

# 驗證碼內會有的符號
CHAR_LIST = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

CAPTCHA_LEN = 4 # 驗證碼長度（６個數字）
CAPTCHA_DIR = f'{current_dir}/CAPTCHA'
TRAIN_CSV = f'{current_dir}/train.csv'
TEST_CSV = f'{current_dir}/test.csv'
IMAGE_WIDTH = 106
IMAGE_HEIGHT = 37
LEARNING_RATE = 0.001
TRAIN_RESULT_PATH = f'{current_dir}/captcha_cnn.pth'
TRAIN_DATA_RATE = 0.9
TEST_DATA_RATE = 0.1
EPOCH = 40
BATCH_SIZE = 200
