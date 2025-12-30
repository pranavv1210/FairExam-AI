"""
PDF and text file parsing utilities
"""

import PyPDF2
import io
import logging
from typing import List

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text content from PDF file
    
    Args:
        pdf_bytes: PDF file content as bytes
        
    Returns:
        Extracted text as string
    """
    try:
        pdf_file = io.BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
        
    except Exception as e:
        logger.error(f"Error extracting PDF text: {e}")
        raise ValueError(f"Failed to parse PDF file: {str(e)}")

def extract_text_from_txt(txt_bytes: bytes) -> str:
    """
    Extract text from text file
    
    Args:
        txt_bytes: Text file content as bytes
        
    Returns:
        Text content as string
    """
    try:
        # Try UTF-8 first, then fall back to latin-1
        try:
            text = txt_bytes.decode('utf-8')
        except UnicodeDecodeError:
            text = txt_bytes.decode('latin-1')
        
        return text.strip()
        
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        raise ValueError(f"Failed to parse text file: {str(e)}")

def parse_document(file_bytes: bytes, filename: str) -> str:
    """
    Parse document based on file type
    
    Args:
        file_bytes: File content as bytes
        filename: Original filename
        
    Returns:
        Extracted text
    """
    filename_lower = filename.lower()
    
    if filename_lower.endswith('.pdf'):
        return extract_text_from_pdf(file_bytes)
    elif filename_lower.endswith('.txt'):
        return extract_text_from_txt(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: {filename}. Only PDF and TXT files are supported.")
