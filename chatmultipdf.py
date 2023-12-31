# -*- coding: utf-8 -*-
"""chatmultipdf.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LAtubP8pII4FfH9P6VOP_zHW2vxtovHB
"""

!pip install langchain
!pip install pypdf
!pip install unstructured
!pip install sentence_transformers
!pip install pinecone-client
!pip install llama-cpp-python
!pip install huggingface_hub

from langchain.document_loaders import PyPDFLoader, OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from sentence_transformers import SentenceTransformer
from langchain.chains.question_answering import load_qa_chain
import pinecone
import os

loader = PyPDFLoader("/content/2308.12261v1.pdf")

loader = PyPDFLoader("/content/2308.13418v1.pdf")

data = loader.load()

data

text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)


docs=text_splitter.split_documents(data)


len(docs)

docs[0]

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_eLonpUwvGKPtZGTywgjBx"
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', 'd2d6c3d-9d50-37a8a0697ed3')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'gcp-starter')

embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_API_ENV
)
index_name = "multipdfchat"

docsearch=Pinecone.from_texts([t.page_content for t in docs], embeddings, index_name=index_name)

query="what is Nougat"


docs=docsearch.similarity_search(query)


docs

from langchain.llms import HuggingFaceHub


llm=HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.1, "max_length":512})


chain=load_qa_chain(llm, chain_type="stuff")


query="Prompting LLMs can be expensive as"
docs=docsearch.similarity_search(query)


chain.run(input_documents=docs, question=query)