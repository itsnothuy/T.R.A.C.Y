import torch
from sentence_transformers import util
import textwrap

class Retriever:
    def __init__(self, embedding_index, similarity_method="dot"):
        """
        embedding_index: an instance of EmbeddingIndex 
                        that has self.embedding_model & self.collection
        similarity_method: 'dot' or 'cosine'
        """
        self.embedding_model = embedding_index.embedding_model
        self.collection = embedding_index.collection
        self.similarity_method = similarity_method
    
    def retrieve_relevant_chunks(self, query: str, top_k: int = 3):
        # Encode query
        query_embedding = self.embedding_model.encode([query])[0]
        
        # If you're using a vector DB like Chroma, the similarity measure is
        # typically determined at index time (dot or cosine).
        # The code below is only for demonstration if you want to do manual scoring.
        
        # In Chroma, we just do:
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )
        
        retrieved_docs = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            retrieved_docs.append((doc, meta))
        return retrieved_docs

def build_context(retrieved_docs: list[tuple[str, dict]]) -> str:
    """
    Combine the retrieved doc texts with metadata into a single context string.
    """
    context_blocks = []
    for i, (doc, meta) in enumerate(retrieved_docs):
        source_info = f"(Source: {meta['source']} - Chunk ID: {meta['chunk_id']})"
        block = f"[{i+1}] {doc}\n{source_info}"
        context_blocks.append(block)
    return "\n\n".join(context_blocks)

def pretty_print_doc(doc_text: str, width=80):
    """
    Simple helper to nicely wrap text for console display.
    """
    return textwrap.fill(doc_text, width=width)

def score_chunks_manual(query_embedding: torch.Tensor, chunk_embeddings: torch.Tensor, method="dot"):
    """
    Illustrative manual scoring function for demonstration.
    method can be 'dot' or 'cosine'
    """
    if method == "dot":
        scores = util.dot_score(query_embedding, chunk_embeddings)[0]
    else:
        scores = util.cos_sim(query_embedding, chunk_embeddings)[0]
    return scores