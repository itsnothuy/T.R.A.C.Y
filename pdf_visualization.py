# pdf_visualization.py
import fitz  # PyMuPDF
import matplotlib.pyplot as plt
import numpy as np

def show_pdf_page(pdf_path: str, page_num: int, dpi: int = 150):
    """
    Loads a page from the PDF and displays it as an image with matplotlib.
    This is mostly for debugging or demonstration.
    """
    doc = fitz.open(pdf_path)
    if page_num < 0 or page_num >= len(doc):
        print(f"Invalid page number: {page_num}")
        return
    page = doc.load_page(page_num)
    pix = page.get_pixmap(dpi=dpi)
    doc.close()

    img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.h, pix.w, pix.n))
    
    plt.figure(figsize=(10, 8))
    plt.imshow(img_array)
    plt.title(f"Page #{page_num}")
    plt.axis("off")
    plt.show()
