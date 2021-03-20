import re
import torch
import numpy as np

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

    
def accuracy(preds, y,lm=False):
    _, indices =preds.max(dim=2) if lm  else preds.max(dim=1)
    correct =(indices.reshape(-1) == y.reshape(-1)).float()
    acc = correct.sum()/len(correct)
    return acc
