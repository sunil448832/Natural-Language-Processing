import re
import json
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
from fastpunct import FastPunct
fastpunct = FastPunct()


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def pad(seq, max_len):
    paddded_seq = seq.copy()
    seq_len = len(seq)
    paddded_seq = paddded_seq+['<pad>']*(max_len-len(seq)) \
        if seq_len < max_len else seq[:max_len]
    return paddded_seq


class MyDataset(Dataset):
    def __init__(self, data, labels):
        super(MyDataset, self).__init__()
        self.data = data
        self.labels = labels

    def __getitem__(self, index):
        return self.data[index], self.labels[index]

    def __len__(self):
        return len(self.data)


class TextLoader:
    def __init__(self):
        self.words = []
        self.vectors = []
        self.word_index = {}
        self.text = []
        self.embed_size = None

    def punc_remove(self, text, correct=False):
        text_seg, text_seg_idx = [], [0]
        for i in range(len(text)):
            text[i] = re.sub(r'[^\w\s\?\.\,]', '', text[i])
            seq = re.split(" and |[^a-zA-Z ]+", text[i])
            seq_ = [i for i in seq if len(i) > 1]
            if len(seq_) < 1:
                seq_.append("unknown")
            text_seg.extend(seq_)
            text_seg_idx.append(text_seg_idx[-1]+len(seq_))

        text_corr = fastpunct.punct(
            text_seg, correct=True) if correct else text_seg

        for i in range(len(text)):
            seq = text_corr[text_seg_idx[i]:text_seg_idx[i+1]]
            text[i] = " ".join(i for i in seq)

        return text

    def glove(self, glove_file):
        with open(glove_file, 'rb') as glove_file:
            for idx, l in enumerate(glove_file):
                line = l.decode().split()
                word, vector = line[0], np.array(line[1:]).astype(np.float)
                self.words.append(word)
                self.vectors.append(vector)
                self.word_index[word] = idx+self.pad_idx

    def tokenize(self, batch, build=False, max_len=100):
        batch_token, batch_index = [], []

        for seq in batch:
            sentence = seq.replace(".", " <eos>")
            tokens = []

            for token in sentence.lower().split(" "):
                try:
                    _ = self.word_index[token]
                    tokens.append(token)
                except KeyError:
                    if build:
                        tokens.append(token)
                        self.words.append(token)
                        self.word_index[token] = len(self.vectors)
                        self.vectors.append(np.random.normal(
                            scale=0.6, size=(self.embed_size, )))
                    elif not build:
                        tokens.append("<unk>")

            if not build:

                tokens = pad(tokens, max_len)
                token_index = [self.word_index[i] for i in tokens]
                batch_token.append(tokens)
                batch_index.append(token_index)

        return batch_token, batch_index

    def build_vocab(self, text, embed_size, vocab_file=None, glove_file=None, write_file=None, correct=False):
        self.embed_size = embed_size
        if vocab_file is not None:
            with open(vocab_file) as file:
                vocab_file_json = json.load(file)
                self.words = vocab_file_json["words"]
                self.word_index = vocab_file_json["word_index"]
                self.vectors = vocab_file_json["vectors"]
                self.text = vocab_file_json["text"]

        else:
            self.word_index['<unk>'] = len(self.vectors)
            self.vectors.append(np.random.normal(
                scale=0.6, size=(embed_size, )))
            self.word_index['<eos>'] = len(self.vectors)
            self.vectors.append(np.random.normal(
                scale=0.6, size=(embed_size, )))
            self.pad_idx = len(self.vectors)
            self.word_index['<pad>'] = self.pad_idx
            self.vectors.append(np.zeros(embed_size))

            if glove_file is not None:
                self.glove(glove_file)
            ds = MyDataset(text, text)
            for txt, _ in tqdm(DataLoader(ds, batch_size=32, shuffle=False)):
                txt = list(txt) if isinstance(txt, tuple) else txt
                text_corr = self.punc_remove(txt, correct)
                self.text.extend(text_corr)
                _, _ = self.tokenize(text_corr, build=True)

            if write_file is not None:
                vocab_file_json = {}
                vocab_file_json["words"] = self.words
                vocab_file_json["word_index"] = self.word_index
                vocab_file_json["vectors"] = self.vectors
                vocab_file_json["text"] = self.text

                with open(write_file, 'w') as file:
                    json.dump(vocab_file_json, file, cls=NumpyEncoder)

    def postprocess(self, batch, max_len=200, correct=False, lm=False):
        batch = list(batch) if isinstance(batch, tuple) else batch
        batch = self.punc_remove(batch, correct)
        if lm:
            _, data_ = self.tokenize(batch, max_len=max_len)
            data_ = np.array(data_)
            data, target = data_[:, :-1], data_[:, 1:]
            return torch.LongTensor(data), torch.LongTensor(target)
        else:
            _, data = self.tokenize(batch, max_len=max_len)
            return torch.LongTensor(data)
