import re
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts all the text from a given PDF file.
    """
    pdf_reader = PdfReader(pdf_path)
    all_text = []
    
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        if text:
            all_text.append(text)
    
    return "\n".join(all_text)

def clean_text(text: str) -> str:
    """
    Basic text cleaning: remove extra newlines, weird chars, etc.
    """
    # Replace multiple newlines or whitespace with a single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    """
    Splits a large text into smaller chunks of size `chunk_size`,
    each chunk overlapping with the next by `overlap` words.
    
    Returns a list of text chunks.
    """
    text = clean_text(text)
    words = text.split(" ")
    chunks = []
    start = 0
    
    while True:
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if not chunk:
            break
        
        chunks.append(chunk)
        start = end - overlap
        if start < 0 or start >= len(words):
            break
    
    return chunks

def create_metadata(chunks: list[str], source_name: str) -> list[dict]:
    """
    Attach metadata (source_name, chunk_id, etc.) to each chunk.
    """
    metadata_chunks = []
    for i, chunk in enumerate(chunks):
        metadata_chunks.append({
            "text": chunk,
            "metadata": {
                "chunk_id": i,
                "source": source_name
            }
        })
    return metadata_chunks
