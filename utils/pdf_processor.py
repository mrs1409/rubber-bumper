import io
import re
import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def process_pdf(file_stream):
    """
    Process a PDF file and extract text chunks.
    
    Args:
        file_stream: A file stream object representing the PDF file.
        
    Returns:
        A list of text chunks, with each chunk containing approximately 1000 characters.
    """
    text = extract_text_from_pdf(file_stream)
    chunks = split_text_into_chunks(text)
    return chunks

def extract_text_from_pdf(file_stream):
    """
    Extract text from a PDF file.
    
    Args:
        file_stream: A file stream object representing the PDF file.
        
    Returns:
        A string containing the extracted text.
    """
    pdf_reader = PyPDF2.PdfReader(file_stream)
    text = ""
    
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text() + "\n"
    
    # Clean the text
    text = clean_text(text)
    
    return text

def clean_text(text):
    """
    Clean the extracted text.
    
    Args:
        text: A string containing the text to clean.
        
    Returns:
        A cleaned string.
    """
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def split_text_into_chunks(text, chunk_size=1000, overlap=200):
    """
    Split text into chunks of approximately chunk_size characters.
    Uses sentence boundaries to ensure chunks don't break in the middle of a sentence.
    
    Args:
        text: A string containing the text to split.
        chunk_size: An integer representing the target size of each chunk.
        overlap: An integer representing the number of characters to overlap between chunks.
        
    Returns:
        A list of text chunks.
    """
    # Split the text into sentences
    sentences = sent_tokenize(text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # If adding the next sentence would exceed the chunk size, 
        # save the current chunk and start a new one
        if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            
            # Start new chunk with overlap from the end of the previous chunk
            # Find the last 'overlap' characters worth of complete sentences
            words = current_chunk.split()
            overlap_text = ""
            for word in reversed(words):
                if len(overlap_text) + len(word) + 1 <= overlap:
                    overlap_text = word + " " + overlap_text
                else:
                    break
            
            current_chunk = overlap_text
        
        current_chunk += " " + sentence
    
    # Add the last chunk if it's not empty
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks
