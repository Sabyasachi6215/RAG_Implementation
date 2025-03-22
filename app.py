import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

# Streamlit app setup
st.set_page_config(page_title="Multi-query Retrieval Demo", layout="wide")
st.title("Multi-query Retrieval for RAG")

# Load and process the PDF
@st.cache_data
def load_and_process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return text_splitter.split_documents(docs)

# Initialize FAISS vectorstore
@st.cache_resource
def setup_vectorstore(documents):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents=documents, embedding=embeddings)
    return vectorstore

# Build Multi-query Retriever
def build_multi_query_retriever(vectorstore):
    llm = ChatOpenAI(temperature=0)
    retriever = MultiQueryRetriever.from_llm(retriever=vectorstore.as_retriever(), llm=llm)
    return retriever

# Main app logic
pdf_path = "india_productivity_2025.pdf"  # Replace with your PDF file path
documents = load_and_process_pdf(pdf_path)
vectorstore = setup_vectorstore(documents)
retriever = build_multi_query_retriever(vectorstore)

# Streamlit input for query
query = st.text_input("Enter your query:")

if query:
    with st.spinner("Generating multiple queries and retrieving documents..."):
        # Retrieve unique documents
        unique_docs = retriever.invoke(query)

        # Display generated queries
        st.subheader("Generated Queries")
        generated_queries = retriever.llm.generate([query])[0]["queries"]
        for i, generated_query in enumerate(generated_queries[:5]):  # Limit to 5 queries
            st.markdown(f"**Query {i+1}:** {generated_query}")

        # Display retrieved documents
        st.subheader("Retrieved Documents")
        for i, doc in enumerate(unique_docs[:5]):  # Limit to 5 documents
            st.markdown(f"**Document {i+1}:**")
            st.write(doc.page_content)
            st.markdown("---")

st.markdown("---")
st.caption("Powered by LangChain, OpenAI, FAISS, and Streamlit")