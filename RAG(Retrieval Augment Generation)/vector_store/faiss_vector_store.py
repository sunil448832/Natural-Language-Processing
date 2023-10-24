import faiss
import numpy as np
import os
import pickle
from tqdm import tqdm

# Create a class for a flat index
class IndexFlat:
    def __init__(self, dimension):
        # Initialize a Faiss flat index with L2 distance
        self.index = faiss.IndexFlatL2(dimension)

    def add(self, vectors):
        # Add vectors to the index
        self.index.add(np.array(vectors))

    def delete(self, ids):
        # Remove vectors from the index by their IDs
        self.index.remove_ids(np.array(ids))

    def search(self, vectors, k):
        # Search for the k-nearest neighbors of the given vectors
        return self.index.search(np.array(vectors), k)

# Create a class for an IVF (Inverted File) index
class IndexIVF:
    def __init__(self, dimension, nlists=100, nprobe=10):
        # Initialize a Faiss flat index and an IVF index with inner product metric
        self.index_flat = faiss.IndexFlatL2(dimension)  
        self.index = faiss.IndexIVFFlat(self.index_flat, dimension, nlists, faiss.METRIC_INNER_PRODUCT)
        self.index.nprobe = nprobe

    def add(self, vectors):
        # Train and add vectors to the index
        self.index.train(np.array(vectors))
        self.index.add(np.array(vectors))

    def delete(self, ids):
        # Remove vectors from the index by their IDs
        self.index.remove_ids(np.array(ids))

    def search(self, vectors, k):
        # Search for the k-nearest neighbors of the given vectors
        return self.index.search(np.array(vectors), k)

# Create a class for managing Faiss vector storage
class FaissVectorStore:
    def __init__(self, dimension=324, nlists=100, nprobe=10):
        self.dimension = dimension
        self.nlists = nlists
        self.nprobe = nprobe
        self.index = None
        self.documents_db = {}

    def add(self, documents):
        ids = range(0, len(self.documents_db) + len(documents))
        db_vectors, db_documents, db_docs_ids = [], [], []

        # Collect existing document vectors and documents
        for doc_id in self.documents_db:
            db_vectors.append(self.documents_db[doc_id]['vector'])
            db_documents.append(self.documents_db[doc_id]['document'])
            db_docs_ids.append(doc_id)

        # Add new document vectors and documents
        for doc_id in documents:
            db_vectors.append(documents[doc_id]['vector'])
            db_documents.append(documents[doc_id]['document'])
            db_docs_ids.append(doc_id)

        if len(db_vectors) < 10000:
            self.index = IndexFlat(self.dimension)
        else:
            self.index = IndexIVF(self.dimension, self.nlists, self.nprobe)

        self.index.add(np.array(db_vectors))
        self.documents_db = {}
        for i, doc_id in enumerate(db_docs_ids):
            self.documents_db[doc_id] = {'vector': db_vectors[i], 'document': db_documents[i], 'index_id': i}
        
    def delete(self, documents_ids):
        # Delete vectors from the index by document IDs
        index_ids_to_delete = []
        for doc_id in documents_ids:
            if doc_id in self.documents_db:
                index_ids_to_delete.append(self.documents_db[doc_id]['index_id'])
        self.index.delete(index_ids_to_delete)
        self.documents_db = {k: v for k, v in self.documents_db.items() if k not in documents_ids}
        

    def query(self, query_vector, k):
        # Query for the top k nearest neighbors to the query_vector
        _, I = self.index.search(query_vector, k)
        documents = []
        for doc_id in self.documents_db:
            if self.documents_db[doc_id]['index_id'] in I[0]:
                documents.append(self.documents_db[doc_id]['document'])
        return documents

    def write(self,database_path):
        # Save the index and documents to files
        if not os.path.exists(database_path):
            os.makedirs(database_path)
        faiss_path = os.path.join(database_path, 'index.faiss')
        document_path = os.path.join(database_path, 'documents.pkl')
        faiss.write_index(self.index.index, faiss_path)
        with open(document_path, 'wb') as f:
            pickle.dump(self.documents_db, f)

    def read(self,database_path):
        # Read the index and documents from files
        faiss_path = os.path.join(database_path, 'index.faiss')
        document_path = os.path.join(database_path, 'documents.pkl')
        self.index = faiss.read_index(faiss_path)
        with open(document_path, 'rb') as f:
            self.documents_db = pickle.load(f)

    @classmethod
    def from_documents(cls, documents, dimension, nlists, nprobe):
        vector_store = cls(dimension, nlists, nprobe)
        vector_store.add(documents)
        return vector_store

    @classmethod
    def as_retriever(cls, database_path):
        vector_store = cls()
        vector_store.read(database_path)
        return vector_store

if __name__ == '__main__':
    nb = 20000
    d = 50
    database_path = 'db_path'

    if not os.path.exists(database_path):
        os.makedirs(database_path)

    documents = {}
    for i in range(nb):
        id = f'id_{i}'
        texts = f'text_{i}'
        vectors = np.random.random((d)).astype('float32')
        documents[id] = {'document': texts, 'vector': vectors}

    vector_store = FaissVectorStore.from_documents(documents, dimension=50, nlists=100, nprobe=10)
    query_vector = np.random.random((1, d)).astype('float32')
    nearest_neighbors = vector_store.query(query_vector, k=5)
    print(nearest_neighbors)
