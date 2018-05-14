## TODO: define the convolutional neural network architecture

import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
# can use the below import should you choose to initialize the weights of your Net
import torch.nn.init as I
import numpy as np


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        
        ## TODO: Define all the layers of this CNN, the only requirements are:
        ## 1. This network takes in a square (same width and height), grayscale image as input
        ## 2. It ends with a linear layer that represents the keypoints
        ## it's suggested that you make this last layer output 136 values, 2 for each of the 68 keypoint (x, y) pairs
        
        # As an example, you've been given a convolutional layer, which you may (but don't have to) change:
        # 1 input image channel (grayscale), 32 output channels/feature maps, 5x5 square convolution kernel
        self.conv1 = nn.Conv2d(1, 32, 5)
        
        ## Note that among the layers to add, consider including:
        # maxpooling layers, multiple conv layers, fully-connected layers, and other layers (such as dropout or batch normalization) to avoid overfitting
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1_drop = nn.Dropout(p=0.4)
        self.conv2 = nn.Conv2d(32, 64, 5)
        self.fc2_drop = nn.Dropout(p=0.4)
        self.conv3 = nn.Conv2d(64, 128, 5)
        self.fc3_drop = nn.Dropout(p=0.4)
        self.fc1 = nn.Linear(128*24*24, 512)
        self.fc4_drop = nn.Dropout(p=0.4)
        self.fc2 = nn.Linear(512, 136)
        
        
        #I.xavier_uniform(self.conv1.weight, gain=I.calculate_gain('relu'))
        #I.xavier_uniform(self.conv2.weight, gain=I.calculate_gain('relu'))
        #I.xavier_uniform(self.conv3.weight, gain=I.calculate_gain('relu'))
        #I.xavier_uniform(self.fc1.weight, gain=I.calculate_gain('relu'))
        #I.xavier_uniform(self.fc2.weight)
        I.xavier_uniform(self.conv1.weight, gain=np.sqrt(2))
        I.xavier_uniform(self.conv2.weight, gain=np.sqrt(2))
        I.xavier_uniform(self.conv3.weight, gain=np.sqrt(2))
        I.xavier_uniform(self.fc1.weight, gain=np.sqrt(2))
        I.xavier_uniform(self.fc2.weight, gain=np.sqrt(2))

       
    def forward(self, x):
        ## TODO: Define the feedforward behavior of this model
        ## x is the input image and, as an example, here you may choose to include a pool/conv step:
        #x = self.pool(nn.LeakyReLU()(self.conv1(x)))
        x = self.pool(F.relu(self.conv1(x)))
        x = self.fc1_drop(x)
        #x = self.pool(nn.LeakyReLU()(self.conv2(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.fc2_drop(x)
        #x = self.pool(nn.LeakyReLU()(self.conv3(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = self.fc3_drop(x)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.fc4_drop(x)
        x = self.fc2(x)
        
        
        # a modified x, having gone through all the layers of your model, should be returned
        return x