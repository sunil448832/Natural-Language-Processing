from models import EmbeddingModel, LLM
from utils import MistralPrompts
from vector_store import FaissVectorStore
import argparse

import warnings
warnings.filterwarnings("ignore")

# Create a ChatBot class to manage interactions
class ChatBot:
    def __init__(self, llm, embedding_model, vector_store):
        self.llm = llm
        self.embedding_model = embedding_model
        self.chat_history = []
        self.vector_store = vector_store

    def format_context(self, retrieved_documents):
        context, sources = '', ''

        # Format retrieved documents into context and sources
        # This is simplest way to combine. there are other techniques as well to try out.
        for doc in retrieved_documents:
            context += doc.text + '\n\n'
            sources += str(doc.metadata) + '\n'

        return context, sources

    def chat(self, question):
        if len(self.chat_history):
            # Create a prompt based on chat history
            chat_history_prompt = MistralPrompts.create_history_prompt(self.chat_history)
            standalone_question_prompt = MistralPrompts.create_standalone_question_prompt(question, chat_history_prompt)
            standalone_question = self.llm.generate_response(standalone_question_prompt)
        else:
            chat_history_prompt = ''
            standalone_question = question

        # Encode the question using the embedding model
        query_embedding = self.embedding_model.encode(standalone_question)

        # Retrieve documents related to the question
        retrieved_documents = self.vector_store.query(query_embedding, 3)
        context, sources = self.format_context(retrieved_documents)

        # Print information about retrieved documents
        print("Retrieved documents info: \n", sources)

        # Create a prompt and generate a response
        prompt = MistralPrompts.create_question_prompt(question, context, chat_history_prompt)
        response = self.llm.generate_response(prompt)

        # Extract the response and update chat history
        response = MistralPrompts.extract_response(response)
        self.chat_history.append((question, response))
        return response

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--vector_database_path", default='vector_db',help="Vector database which store embeddings vector")
    args = parser.parse_args()

    VECTOR_DATABASE_PATH = parser.vector_database_path
    # Initialize models and vector store
    embedding_model = EmbeddingModel(model_name='sentence-transformers/all-MiniLM-L6-v2')
    llm = LLM("mistralai/Mistral-7B-Instruct-v0.1")
    vector_store = FaissVectorStore.as_retriever(database_path=VECTOR_DATABASE_PATH)

    # Create a ChatBot instance
    chat_bot = ChatBot(llm, embedding_model, vector_store)

    # Start the conversation
    print("Assistant Bot: Hello, I'm the Assistant Bot! How may I assist you today?")
    while True:
        question = input("User:")
        response = chat_bot.chat(question)
        print("Assistant Bot:", response, '\n')
