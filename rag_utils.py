# rag_utils.py

import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

from datasets import load_dataset

# 1) Load a QA dataset (e.g., SQuAD) and prepare text chunks
def load_and_chunk_squad_dataset():
    """
    Loads a portion of the SQuAD dataset, extracts contexts, and returns them as a list of strings.
    In real usage, you'd do more advanced chunking (500-1000 tokens per chunk).
    """
    squad_data = load_dataset("squad", split="train[:1%]")  # Just 1% for demo
    
    # Extract contexts from the dataset
    # Each entry has: {id, title, context, question, answers}
    # We'll treat 'context' as chunks to store in the vector DB
    contexts = []
    for item in squad_data:
        context_text = item["context"]
        # You might do more sophisticated chunking here if the context is large
        contexts.append(context_text)
    return contexts

# 2) Build or load a vector store with embeddings
def build_vectorstore_from_contexts(contexts, collection_name="qa_collection"):
    """
    Create a Chroma vector store from a list of context texts.
    You can also persist this to disk if you want to avoid rebuilding each time.
    """
    # Option A: Use OpenAI embeddings
    embeddings = OpenAIEmbeddings()  # needs OPENAI_API_KEY in env

    # Optionally, if you don't want to use OpenAI:
    # from langchain.embeddings import HuggingFaceEmbeddings
    # embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Build Chroma in-memory (for demo)
    vectorstore = Chroma.from_texts(contexts, embeddings, collection_name=collection_name)
    return vectorstore

# 3) Create a retrieval-based QA chain
def create_rag_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})  # retrieve top 3 chunks

    # Use GPT-3.5 or GPT-4 for generation
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",  # or "gpt-4" if you have access
    )

    # Build a RetrievalQA chain
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )
    return rag_chain

# 4) High-level function that returns an answer to user queries
def get_rag_answer(user_query, rag_chain):
    """
    Takes a user_query (string) and uses the RAG chain to retrieve relevant context + generate an answer.
    """
    answer = rag_chain.run(user_query)
    return answer
