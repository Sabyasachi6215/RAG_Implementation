
import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chat_models import ChatOpenAI  # Import ChatOpenAI
from dotenv import load_dotenv
import logging
import os
from langchain_openai import OpenAIEmbeddings
load_dotenv()

loader = PyPDFLoader("india_productivity_2025.pdf")  # Replace with your PDF file path
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splitter = text_splitter.split_documents(docs)
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents=splitter, embedding=embeddings)

from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI

question = "What is India seen in 2025?"
llm = ChatOpenAI(temperature=0)
retriever_from_llm = MultiQueryRetriever.from_llm(retriever=vectorstore.as_retriever(), llm=llm)
import logging

logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)
unique_docs = retriever_from_llm.invoke(question)
len(unique_docs)

print(unique_docs)


