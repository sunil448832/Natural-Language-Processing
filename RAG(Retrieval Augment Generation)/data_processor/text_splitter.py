from dataclasses import dataclass
import re

# Data class for representing a text split
@dataclass
class Split:
    text: str  # the split text
    is_sentence: bool  # save whether this is a full sentence

# Data class for representing a document
@dataclass
class Document:
    doc_id: str
    text: str
    metadata: dict

# Class for splitting text into sentences
class SentenceSplitter:
    def __init__(self, chunk_size=100, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # List of functions for splitting text
        self._split_fn_sentence = [self._split_by_sep('\n\n'), self._split_by_regex("[^,.;。？！]+[,.;。？！]?")]
        self._split_fn_subsentence = [self._split_by_sep(' ')]

    def _split_by_sep(self, sep):
        # Split text by separator and maintain the separator
        def fun(text):
            parts = text.split(sep)
            result = [sep + s if i > 0 else s for i, s in enumerate(parts)]
            return [s for s in result if s]
        return lambda text: fun(text)

    def _split_by_regex(self, regex):
        # Split text using a regular expression
        return lambda text: re.findall(regex, text)

    def _splits_by_fns(self, text):
        for split_fn in self._split_fn_sentence:
            splits = split_fn(text)
            if len(splits) > 1:
                return splits, True

        for split_fn in self._split_fn_subsentence:
            splits = split_fn(text)
            if len(splits) > 1:
                break

        return splits, False

    def _token_size(self, text):
        # Calculate the token size of text
        return len(text.split(' '))

    def _split(self, text, chunk_size):
        # Break text into splits that are smaller than chunk size
        if self._token_size(text) <= chunk_size:
            return [Split(text, is_sentence=True)]

        text_splits = []
        text_splits_by_fns, is_sentence = self._splits_by_fns(text)
        for text_split_by_fns in text_splits_by_fns:
            if self._token_size(text_split_by_fns) <= chunk_size:
                text_splits.append(Split(text_split_by_fns, is_sentence=is_sentence))
            else:
                recursive_text_splits = self._split(text_split_by_fns, chunk_size=chunk_size)
                text_splits.extend(recursive_text_splits)
        return text_splits

    def _merge(self, splits, chunk_size):
        # Merge splits into chunks
        chunks, cur_chunk, last_chunk = [], [], []
        cur_chunk_len = 0
        new_chunk = True

        def close_chunk():
            nonlocal chunks, cur_chunk, last_chunk, cur_chunk_len, new_chunk

            chunks.append("".join([text for text, length in cur_chunk]))
            last_chunk = cur_chunk
            cur_chunk = []
            cur_chunk_len = 0
            new_chunk = True
            # Add overlap to the new chunk from previous chunks
            if len(last_chunk) > 0:
                last_index = len(last_chunk) - 1
                while (
                    last_index >= 0
                    and cur_chunk_len + last_chunk[last_index][1] <= self.chunk_overlap
                ):
                    text, length = last_chunk[last_index]
                    cur_chunk_len += length
                    cur_chunk.insert(0, (text, length))
                    last_index -= 1

        while len(splits) > 0:
            cur_split = splits[0]
            cur_split_len = self._token_size(cur_split.text)

            # Close the chunk if it exceeds chunk_size
            if cur_chunk_len + cur_split_len > chunk_size and not new_chunk:
                close_chunk()
            else:
                if (
                    cur_split.is_sentence
                    or cur_chunk_len + cur_split_len <= chunk_size
                    or new_chunk  # new chunk, always add at least one split
                ):
                    # Add split to chunk
                    cur_chunk_len += cur_split_len
                    cur_chunk.append((cur_split.text, cur_split_len))
                    splits.pop(0)
                    new_chunk = False
                else:
                    # Close out the chunk
                    close_chunk()

        # Handle the last chunk
        if not new_chunk:
            chunk = "".join([text for text, length in cur_chunk])
            chunks.append(chunk)

        # Run post-processing to remove blank spaces
        new_chunks = [chunk.strip() for chunk in chunks if chunk.strip() != ""]
        return new_chunks

    def split_texts(self, documents):
        chunked_documents = []
        for page_no, document in enumerate(documents):
            text, metadata = document['text'], document['metadata']
            if text == "":
                continue
            splits = self._split(text, self.chunk_size)
            chunks = self._merge(splits, self.chunk_size)
            for chunk_no, chunk in enumerate(chunks):
                chunk_id = f"{metadata['file_name']}__{page_no}__{chunk_no}"
                chunk_metadata = {'file_name': metadata['file_name'], 'page_no': page_no, 'chunk_no': chunk_no}
                data = Document(chunk_id, chunk, chunk_metadata)
                chunked_documents.append(data)
        return chunked_documents

if __name__ == '__main__':
    document = {
        "text": "This is example texts",
        "metadata": {"file_name": "example.pdf", "page_no": 1}
    }
    documents = [document] * 10
    splitter = SentenceSplitter(chunk_size=100, chunk_overlap=30)
    splitted_documents = splitter.split_texts(documents)

    print(splitted_documents[0])
