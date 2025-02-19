from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

class EmbeddingIndex:
    def __init__(self, embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
                 persist_directory="chroma_db", collection_name="my_collection"):
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model_name, device="cpu")
        
        # Initialize Chroma DB client
        self.chroma_client = chromadb.Client(
            Settings(
                persist_directory=persist_directory,
                # No 'chroma_db_impl' line here
            )
        )
        
        # Create or retrieve collection
        self.collection = self.chroma_client.get_or_create_collection(collection_name)
    
    def compute_embeddings(self, texts: list[str]):
        """
        Compute embeddings for a list of texts using the loaded embedding model.
        """
        return self.embedding_model.encode(texts, show_progress_bar=True)
    
    def add_to_index(self, texts: list[str], embeddings, metadatas: list[dict], ids: list[str]):
        """
        Add documents, embeddings, and metadata to the Chroma collection.
        """
        self.collection.add(
            documents=texts,
            embeddings=[emb.tolist() for emb in embeddings],
            metadatas=metadatas,
            ids=ids
        )
    
    def persist(self):
        """Persist the current state of the database to disk."""
        # For Chroma, if using persistent mode, it should auto-persist.
        # But you can explicitly call a persist method if needed.
        pass
    
    def load(self):
        """
        Reload or get the existing collection from the DB.
        Not always required, but can be used if you need to refresh.
        """
        # Implementation depends on your vector DB.
        pass
