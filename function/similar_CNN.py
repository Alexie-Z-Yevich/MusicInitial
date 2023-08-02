import torch
import torch.nn as nn

class YourCNN(nn.Module):
    def __init__(self, num_features):
        super(YourCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=(3, 3), stride=(1, 1))
        self.pool = nn.MaxPool2d(kernel_size=(2, 2))
        self.conv2 = nn.Conv2d(16, 32, kernel_size=(3, 3), stride=(1, 1))
        self.avgpool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Linear(32, 1)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = torch.sigmoid(self.fc(x))
        return x

def similar_CNN(target_mfcc, b_mfcc):
    # 创建模型实例
    num_features = target_mfcc.shape[1]
    model = YourCNN(num_features)

    # 将MFCC特征转换为张量
    target_mfcc_tensor = torch.tensor(target_mfcc).unsqueeze(0).unsqueeze(1).float()
    b_mfcc_tensor = torch.tensor(b_mfcc).unsqueeze(0).unsqueeze(1).float()

    # 将特征输入模型进行前向传播
    target_output = model(target_mfcc_tensor)
    b_output = model(b_mfcc_tensor)

    # 计算近似相关度
    similarity = torch.abs(target_output - b_output)

    # 返回相关度值
    return similarity.item()