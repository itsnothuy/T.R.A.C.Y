# main.py
from data_ingestion import (
    extract_text_from_pdf,
    chunk_text,
    create_metadata,
    explore_text_chunks,
    chunk_text_spacy
)
from embeddings_indexing import EmbeddingIndex
from retrieval import Retriever, build_context, pretty_print_doc
from prompt_inference import LocalLLMInference, build_prompt_with_examples
from attribution import format_answer_with_references
import random
import torch
def main():
    # 1) Data ingestion
    pdf_path = "2.pdf"
    raw_text = extract_text_from_pdf(pdf_path)
    
    # CHOOSE your chunking method:
    # Option A: Word-based chunking
    # chunks = chunk_text(raw_text, chunk_size=300, overlap=50)
    
    # Option B: Sentence-based chunking with spaCy
    chunks = chunk_text_spacy(raw_text, sentences_per_chunk=10, min_length=30)
    
    metadata_chunks = create_metadata(chunks, source_name=pdf_path)
    
    # Optional: explore to see random samples & stats
    explore_text_chunks(metadata_chunks, n_samples=3)
    
    # 2) Embeddings & Index
    embedding_index = EmbeddingIndex(
        embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
        persist_directory="chroma_db",
        collection_name="nutrition_collection"
    )
    
    all_texts = [item["text"] for item in metadata_chunks]
    all_metadatas = [item["metadata"] for item in metadata_chunks]
    all_ids = [f"chunk_{m['chunk_id']}" for m in all_metadatas]
    
    embeddings = embedding_index.compute_embeddings(all_texts)
    embedding_index.add_to_index(all_texts, embeddings, all_metadatas, all_ids)
    
    # 3) Retrieval
    retriever = Retriever(embedding_index=embedding_index, similarity_method="dot")
    
    # We'll pick a random user query for demonstration
    example_queries = [
        "What is the role of Vitamin D in bone health?",
        "How does fiber help in digestion?",
        "What are the fat-soluble vitamins?",
        "What is the recommended daily intake for protein?"
    ]
    user_query = random.choice(example_queries)
    print(f"\nUser query: {user_query}\n")
    
    top_docs = retriever.retrieve_relevant_chunks(user_query, top_k=3)
    
    # Print them for debugging
    for i, (doc, meta) in enumerate(top_docs):
        print(f"=== Top Doc #{i+1} ===")
        print(pretty_print_doc(doc[:500]))
        print(f"Metadata: {meta}\n")
    
    # Build final context
    context_for_llm = build_context(top_docs)
    
    # 4) Prompt & Inference
    final_prompt = build_prompt_with_examples(context_for_llm, user_query)
    print("Prompt:\n", final_prompt)
    
    local_llm = LocalLLMInference(
        model_name="tiiuae/falcon-7b-instruct",
        device_map="cpu",  # or "mps" for Apple M1
        torch_dtype=torch.float32  # or torch.float16
    )
    raw_answer = local_llm.generate_answer(final_prompt, temperature=0.5, top_p=0.9)
    
    # 5) Attribution
    final_output = format_answer_with_references(raw_answer, top_docs)
    print("\n\n=== Final Answer ===")
    print(final_output)

if __name__ == "__main__":
    main()
