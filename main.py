# main.py (excerpt)
from embeddings_indexing import EmbeddingIndex

# Suppose you have metadata_chunks from previous steps
all_texts = [item["text"] for item in metadata_chunks]
all_metadatas = [item["metadata"] for item in metadata_chunks]
all_ids = [f"chunk_{m['chunk_id']}" for m in all_metadatas]

# Initialize
embedding_index = EmbeddingIndex(
    embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
    persist_directory="chroma_db",
    collection_name="nutrition_collection"
)

embeddings = embedding_index.compute_embeddings(all_texts)
embedding_index.add_to_index(all_texts, embeddings, all_metadatas, all_ids)
embedding_index.persist()


# main.py (excerpt)
from prompt_inference import LocalLLMInference, build_prompt

# Suppose context_for_llm is from retrieval
final_prompt = build_prompt(context_for_llm, user_query)

# Initialize the LLM
local_llm = LocalLLMInference(
    model_name="tiiuae/falcon-7b-instruct",
    device_map="mps", 
    torch_dtype=torch.float16
)

answer = local_llm.generate_answer(final_prompt)
print(answer)


# main.py (excerpt)
from attribution import format_answer_with_references

final_output = format_answer_with_references(answer, top_docs)
print(final_output)