from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

def retriever(file_path, k=2):
    assert file_path.endswith('.pdf'), "PDF files are the only supported format"
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()

    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    embedding_model = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    faiss_index = FAISS.from_documents(pages, embedding_model)
    retriever = faiss_index.as_retriever(search_kwargs={"k": k})

    return retriever
