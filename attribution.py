def format_answer_with_references(raw_answer: str, retrieved_docs: list[tuple[str, dict]]) -> str:
    """
    For demonstration: a naive approach to highlight chunk references 
    directly in the final answer.
    """
    # Maybe check for "[1]", "[2]" in raw_answer
    # Then append real references at the bottom.
    
    references = []
    for i, (doc, meta) in enumerate(retrieved_docs):
        ref_text = f"[{i+1}] Source: {meta['source']}, Chunk ID: {meta['chunk_id']}"
        references.append(ref_text)
    
    references_str = "\n".join(references)
    final_answer = f"{raw_answer}\n\nReferences:\n{references_str}"
    return final_answer
