from flask import Flask, request, jsonify
from dotenv import load_dotenv

from langchain.memory import ConversationBufferMemory
from chain import llm_chain
from ingest import retriever

# Load variables from the .env file into the environment
app = Flask(__name__)

load_dotenv()
@app.route('/upload', methods=['POST'])
def upload_file():
    file_path = request.json.get('file_path')
    global  retriever_
    retriever_=retriever(file_path,k=2)

    return "File Uploaded Sucsesfully"
@app.route('/chat', methods=['POST'])
def chat():
    questions = request.json.get('questions')
    memory = ConversationBufferMemory()
    chain=llm_chain(retriever_,memory)
    
    quation_answer=""
    for question in questions.split('\n'):
      inputs = {"question": question}
      result = chain.invoke(inputs)
      quation_answer+=f"Question: {question} <br> Answer: {result['answer'].content} <br><br>"
      memory.save_context(inputs, {"answer": result["answer"].content})
    
    return jsonify({'quation_answer': quation_answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
