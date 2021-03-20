import torch
from torch.autograd import Variable
import torch.nn as nn

class BaseModel(nn.Module):
  def __init__(self,vocab_size,embedding_size,hidden_size,weights=None,dropout=.3):
    super(BaseModel,self).__init__()
    self.hidden_size=hidden_size
    self.embedding = nn.Embedding(vocab_size, embedding_size)
    if weights is not None:
      self.embedding.load_state_dict({'weight': torch.FloatTensor(weights)})
      self.embedding.weight.requires_grad = False
    self.lstm= nn.LSTM(embedding_size, hidden_size // 2,num_layers=1, bidirectional=True,batch_first=True)
    self.drop = nn.Dropout(dropout)
    self.rnn_state=None
  
  def repackage_rnn_state(self):
    self.rnn_state = self._detach_rnn_state(self.rnn_state)

  def _detach_rnn_state(self, h):
    if isinstance(h, torch.Tensor):
      return h.detach()
    else:
      return tuple(self._detach_rnn_state(v) for v in h)

  def forward(self,input):
    embedded = self.embedding(input)
    embedded=self.drop(embedded)
    out,self.rnn_state= self.lstm(embedded,self.rnn_state)
    return out
