from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict
from collections import defaultdict
from transformers import pipeline
import pickle

# Create a cache for PDF data in memory
pdf_cache = {}
qa_pipeline = pipeline("question-answering", model="deepset/bert-base-cased-squad2")

def load_and_cache_pdf(file_path: str):
    """Load PDF data and cache it."""
    # Check if the PDF data is already cached
    if file_path in pdf_cache:
        print(f"Using cached data for {file_path}")
        return pdf_cache[file_path]

    # Load the PDF file and split it into chunks
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    texts = text_splitter.split_documents(pages)

    # Combine all the text chunks into a single text block
    final_texts = ""
    for text in texts:
        final_texts += text.page_content

    # Cache the PDF data in memory
    pdf_cache[file_path] = final_texts

    return final_texts

def search_pdf_data(pdf_data: str, question: str) -> str:
    """Search PDF data for the answer to the given question."""
    # This is a basic keyword search.
    # You may want to use a more advanced search algorithm for better results.
    # For now, we use a simple string search.
    search_result = []
    keywords = question.lower().split()

    for line in pdf_data.split('\n'):
        if any(keyword in line.lower() for keyword in keywords):
            search_result.append(line)

    # Combine search results into a single string
    answer = ' '.join(search_result[:1])  # Return the first matching line as the answer

    return answer if answer else "No answer found in PDF."

def search(file_path: str, question: str) -> str:
    """Search the PDF file for the answer to the given question."""
    # Load and cache the PDF data
    pdf_data = load_and_cache_pdf(file_path)

    # Search the cached PDF data
    answer = search_pdf_data(pdf_data, question)

    return answer

# Example usage
if __name__ == '__main__':
    file_path = "C:/Users/Rohith/OneDrive/Documents/Roas-app/Roas-app/tnbook.pdf"
    question = "What is photosynthesis?"
    answer = search(file_path, question)
    print("PDF Answer:")
    print(answer)
