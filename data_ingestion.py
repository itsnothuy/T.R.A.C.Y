import re
from pypdf import PdfReader
import pandas as pd
import spacy
import random
import textwrap

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts all the text from a given PDF file using pypdf.
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
    Basic text cleaning: remove extra newlines or excessive whitespace, etc.
    """
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    """
    Splits large text into word-based chunks.
    Each chunk has up to `chunk_size` words, and
    overlaps with the next chunk by `overlap` words.
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

def split_into_sentences_spacy(text: str) -> list[str]:
    """
    Uses spaCy to split text into sentences more robustly than naive splitting.
    """
    nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger", "ner"])
    if "sentencizer" not in nlp.pipe_names:
        nlp.add_pipe("sentencizer")
    doc = nlp(text)
    return [str(sent).strip() for sent in doc.sents]

def chunk_text_spacy(
    text: str,
    sentences_per_chunk: int = 10,
    min_length: int = 30
) -> list[str]:
    """
    Splits text into sentences using spaCy, then groups them into
    chunks of `sentences_per_chunk` each. Filters out short chunks.
    """
    text = clean_text(text)
    all_sentences = split_into_sentences_spacy(text)
    
    # group sentences in increments of `sentences_per_chunk`
    def group_list(lst, size):
        return [lst[i:i+size] for i in range(0, len(lst), size)]
    
    sentence_groups = group_list(all_sentences, sentences_per_chunk)
    
    chunks = []
    for group in sentence_groups:
        combined = " ".join(group)
        if len(combined.split()) >= min_length:  # filter out tiny chunks
            chunks.append(combined)
    
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

def explore_text_chunks(chunks_list: list[dict], n_samples: int = 3):
    """
    Prints basic stats using pandas describe() plus
    a few random samples for a quick sanity check.
    """
    df = pd.DataFrame(chunks_list)
    # If there's a 'text' field, measure length
    if "text" in df.columns:
        df["token_estimate"] = df["text"].apply(lambda t: len(t) / 4.0)
    print(df.describe().round(2))
    
    print("\nSample chunks:\n")
    for row in random.sample(chunks_list, k=min(n_samples, len(chunks_list))):
        snippet = textwrap.fill(row["text"][:300], width=70)
        print(f"Chunk ID: {row['metadata']['chunk_id']}, Source: {row['metadata']['source']}")
        print("Snippet:", snippet, "...\n", "-"*50)
