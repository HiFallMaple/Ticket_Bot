import logging
from torchvision import transforms

logging.basicConfig(level=logging.INFO)

# 驗證碼內會有的符號
CHAR_LIST = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

CAPTCHA_LEN = 4 # 驗證碼長度（６個數字）
CAPTCHA_DIR = 'CAPTCHA'
TRAIN_CSV = 'train.csv'
TEST_CSV = 'train.csv'
IMAGE_WIDTH = 1065
IMAGE_HEIGHT = 375
LEARNING_RATE = 0.001
TRAIN_RESULT_PATH = './captcha_cnn.pth'
TRAIN_DATA_RATE = 0.025
TEST_DATA_RATE = 0.1
EPOCH = 10

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])