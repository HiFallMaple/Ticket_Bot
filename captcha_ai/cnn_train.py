# pytorch
import torch
from torch import nn
from torch.autograd import Variable
from torch.utils.data import DataLoader
from . import config
from .cnn_dataset import CAPTCHADataset
from .cnn_model import CNN

# import random_files




device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f'Using {device} device')

cnn = CNN().to(device)
cnn.load_state_dict(torch.load(config.TRAIN_RESULT_PATH))

train_dataset = CAPTCHADataset(config.TRAIN_CSV, config.CAPTCHA_DIR)
train_dataloader = DataLoader(train_dataset, batch_size=config.BATCH_SIZE)

validation_dataset = CAPTCHADataset(config.TEST_CSV, config.CAPTCHA_DIR)
validation_dataloader = DataLoader(validation_dataset, batch_size=config.BATCH_SIZE)

criterion = nn.MultiLabelSoftMarginLoss()
optimizer = torch.optim.Adam(cnn.parameters(), lr=config.LEARNING_RATE)

for epoch in range(config.EPOCH):
    for i, (images, labels) in enumerate(train_dataloader):
        images = Variable(images).to(device)
        labels = Variable(labels.float()).to(device)
        predict_labels = cnn(images)
        # print(predict_labels.type)
        # print(labels.type)
        loss = criterion(predict_labels, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if (i+1) % 10 == 0:
            print("epoch:", epoch, "step:", i, "loss:", loss.item())
    print("epoch:", epoch, "step:", i, "loss:", loss.item())
    torch.save(cnn.state_dict(), f"{config.TRAIN_RESULT_PATH}_epoch{epoch}")


print('Finished Training')
torch.save(cnn.state_dict(), config.TRAIN_RESULT_PATH)
