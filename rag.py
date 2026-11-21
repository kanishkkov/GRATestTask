
from pathlib import Path
import pymupdf  # PyMuPDF

## Function to load documents from a specified directory and extract text from each page of PDF files.
def load_documents(directory="documents"):
    pages = []

    for pdf_path in sorted(Path(directory).glob("*.pdf")):
        doc = pymupdf.open(pdf_path)

        for page_num, page in enumerate(doc, start=1):
            text = page.get_text().strip()

            if text:
                pages.append({
                    "source": pdf_path.name,
                    "page": page_num,
                    "text": text
                })

        doc.close()

    return pages

#Function to chunk the extracted text from each page into smaller segments based on specified chunk size and overlap.
def chunk_documents(pages, chunk_size=800, overlap=150):
    chunks = []

    for page in pages:
        text = " ".join(page["text"].split())

        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))

            chunks.append({
                "source": page["source"],
                "page": page["page"],
                "text": text[start:end]
            })

            if end == len(text):
                break

            start = end - overlap

    return chunks


if __name__ == "__main__":
    pages = load_documents()
    chunks = chunk_documents(pages)

    print(f"Loaded {len(pages)} pages")
    print(f"Created {len(chunks)} chunks")

    if chunks:
        print("\nFirst chunk:")
        print(chunks[0])
