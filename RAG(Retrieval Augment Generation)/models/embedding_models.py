import torch
from transformers import AutoTokenizer, AutoModel
import torch.nn.functional as F

# Create a class for embedding sentences using Hugging Face Transformers
class EmbeddingModel:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        # Initialize the model with the given model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        # Get the embedding dimension from the model's output
        self.embedding_dim = self.encode('Hi').shape[1]

    def _mean_pooling(self, model_output, attention_mask):
        # Calculate mean pooling of token embeddings
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        embedding = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return embedding

    def encode(self, text):
        # Encode a text into sentence embeddings
        inputs = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            outputs = self.model(**inputs)
        sentence_embeddings = self._mean_pooling(outputs, inputs['attention_mask'])
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1).numpy().astype('float32')
        return sentence_embeddings
    
if __name__ == '__main__':
    # Sentences we want sentence embeddings for
    sentences = ['This is an example sentence', 'Each sentence is converted']
    # Print the embedding dimension of the model
    print(EmbeddingModel().embedding_dim)

