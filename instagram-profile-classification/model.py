import gensim
from gensim.models import KeyedVectors
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import gensim
import umap
import hdbscan
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from statistics import mode
import os
import gdown

class classifyProfile:
  def __init__(self,labels=None):
    google_drive_url = 'https://drive.google.com/uc?id=0B7XkCwpI5KDYNlNUTTlSS21pQmM'
    os.makedirs('weights', exist_ok=True)
    model_path = 'weights/GoogleNews-vectors-negative300.bin.gz'

    if not os.path.exists(model_path):
        gdown.download(google_drive_url, model_path, quiet=False)
        print(f"Weights downloaded and saved as {model_path}")
    else:
        print(f"Weights already exists at {model_path}. Skipping download.")
    
    nltk.download('stopwords')
    nltk.download('punkt')
    self.model = KeyedVectors.load_word2vec_format(model_path, binary=True)
    self.labels=labels
    if not self.labels:
      self.labels=["travel", "food", "fashion", "technology", "fitness",'others']
    

      
  def preprocess_text(self,text):
      # Tokenize and remove punctuation
      tokens = word_tokenize(text.lower())
      tokens = [word for word in tokens if word.isalnum()]

      # Remove stopwords
      stop_words = set(stopwords.words('english'))
      tokens = [word for word in tokens if word not in stop_words]

      return tokens

  def generate_substrings(self,input_string,vocabulary):
      substrings = []
      n = len(input_string)
      for i in range(n):
          for j in range(i + 1, n + 1):
              substr=input_string[i:j]
              if substr in vocabulary:
                substrings.append(substr)
      substrings=sorted(substrings,key =lambda x:len(x),reverse =True)
      return substrings[:3]

  def get_word_embeddings(self,words):
    word_embeddings={}
    for word in words:
      if word in self.model:
        word_embeddings[word] = self.model[word]
      else:
        valid_substrings=self.generate_substrings(word, self.model)
        for substr in valid_substrings:
          if len(substr)>3:
            word_embeddings[substr] = self.model[substr]
    return word_embeddings
    
  def nearest_label(self,labels_vectors,topic_vectors):
    final_label=[]
    for cluster, topic_vector in topic_vectors.items():
      closest_labels=[[cosine_similarity([labels_vectors[label]],[topic_vector])[0],label] for label in labels_vectors]
      closest_labels=sorted(closest_labels,reverse=True)
      final_label.append(closest_labels[0][1])
    label = mode(final_label)
    return label

  def classify(self,documents):
    document_embeddings_org,document_embeddings_comp,document_words=[],[],[]
    umap_model = umap.UMAP(n_components=5, metric='cosine', random_state=42)
    for document in documents:
      try:
        words=self.preprocess_text(document)
        word_embeddings = self.get_word_embeddings(words)
        emb=np.array(list(word_embeddings.values()))
        word_embeddings_comp = umap_model.fit_transform(emb)
        document_embeddings_org.extend(word_embeddings.values())
        document_embeddings_comp.extend(word_embeddings_comp)
        document_words.extend(word_embeddings.keys())
      except:
        print("---------problem in converting in lower dimention----------------")
        pass
    label_vectors = self.get_word_embeddings(self.labels)

    clusterer = hdbscan.HDBSCAN(min_cluster_size=6, metric='euclidean', cluster_selection_method='eom')
    document_labels = clusterer.fit_predict(document_embeddings_comp)

    unique_clusters = set(document_labels)
    topic_vectors = {}
    for cluster in unique_clusters:
      if cluster != -1:
        cluster_mask = (document_labels == cluster)
        cluster_documents = np.array(document_embeddings_org)[cluster_mask]
        topic_vector = np.mean(cluster_documents, axis=0)
        topic_vectors[cluster] = topic_vector

    label=self.nearest_label(label_vectors,topic_vectors)
    return label
