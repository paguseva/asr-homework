import torch
import torch.nn as nn
import torch.nn.functional as F


def get_same_padding(kernel_size, dilation=1):
    if dilation > 1:
        return (dilation * kernel_size) // 2 - 1
    return kernel_size // 2
