from data_processor import DocumentReader, SentenceSplitter
from models import EmbeddingModel
from vector_store import FaissVectorStore
from tqdm import tqdm
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", default='data/KnowledgeDocument(pan_card_services).txt',help="Input file name")
    parser.add_argument("--vector_database_path", default='vector_db',help="Vector database which store embeddings vector")
    args = parser.parse_args()

    # Define the paths to the data and vector database
    DATA_PATH = args.data_path
    VECTOR_DATABASE_PATH = args.vector_database_path

    # Read the document from the specified path
    documents = DocumentReader.read_document(DATA_PATH)

    # Split the document into sentences with specified chunk parameters
    splitter = SentenceSplitter(chunk_size=60, chunk_overlap=20)
    splitted_documents = splitter.split_texts(documents)

    # Initialize the embedding model
    embedding_model = EmbeddingModel(model_name='sentence-transformers/all-MiniLM-L6-v2')

    # Create a dictionary to store documents and their corresponding vectors
    database_documents = {}
    batch_size = 16
    print("Generating embedding vectors....")
    # Process the documents in batches
    for i in tqdm(range(0, len(splitted_documents), batch_size)):
        batch = splitted_documents[i:i + batch_size]
        texts = []
        
        # Extract the text from each document in the batch
        for b in batch:
            texts.append(b.text)

        # Generate embeddings for the batch of texts using the embedding model
        embeddings = embedding_model.encode(texts)

        # Associate each document with its corresponding vector and store in the dictionary
        for i, b in enumerate(batch):
            data = {'document': b, 'vector': embeddings[i]}
            database_documents[b.doc_id] = data
    print("Total embeddings: ",len(database_documents))
    # Create a Faiss vector store from the processed documents and vectors
    vector_store = FaissVectorStore.from_documents(database_documents, dimension=embedding_model.embedding_dim, nlists=100, nprobe=10)

    # Write the vector store to the specified path
    vector_store.write(VECTOR_DATABASE_PATH)
    print(f"Successfully written embedding vectors to {VECTOR_DATABASE_PATH} .")
