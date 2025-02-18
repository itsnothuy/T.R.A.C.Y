class Retriever:
    def __init__(self, embedding_index):
        """
        embedding_index: an instance of EmbeddingIndex 
                        that has self.embedding_model & self.collection
        """
        self.embedding_model = embedding_index.embedding_model
        self.collection = embedding_index.collection
    
    def retrieve_relevant_chunks(self, query: str, top_k: int = 3):
        query_embedding = self.embedding_model.encode([query])[0].tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        # results => { "documents": [...], "metadatas": [...], "embeddings": [...], "ids": [...] }
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
