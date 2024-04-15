# Importing necessary modules from Flask and other libraries
from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain.vectorstores import Pinecone
import pinecone
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from src.prompt import *  # Assuming `prompt_template` is defined in this module
import os

# Creating a Flask app instance
app = Flask(__name__)

# Loading environment variables from the .env file
load_dotenv()

# Retrieving Pinecone API key and environment from environment variables
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')

# Downloading Hugging Face embeddings
embeddings = download_hugging_face_embeddings()

# Initializing Pinecone with API key and environment
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)

# Specifying the name of the index
index_name = "medical-bot"

# Loading the index using Pinecone
docsearch = Pinecone.from_existing_index(index_name, embeddings)

# Defining a prompt template for the conversation
PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# Configuring parameters for the language model and retrieval QA chain
chain_type_kwargs = {"prompt": PROMPT}

# Initializing the language model
llm = CTransformers(model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
                    model_type="llama",
                    config={'max_new_tokens': 512, 'temperature': 0.8})

# Initializing the RetrievalQA chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)

# Route for rendering the chat interface
@app.route("/")
def index():
    return render_template('chat.html')

# Route for handling chat messages
@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result = qa({"query": input})  # Performing the retrieval QA
    print("Response : ", result["result"])
    return str(result["result"])

# Running the Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
