"""
Text cleaning and preprocessing utilities
"""

import re
from typing import List

def clean_text(text: str) -> str:
    """
    Clean and normalize text
    
    Args:
        text: Raw text
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s\.,;:?!()\-\'\"]+', ' ', text)
    
    # Remove multiple spaces
    text = ' '.join(text.split())
    
    return text.strip()

def extract_questions(exam_text: str) -> List[str]:
    """
    Extract individual questions from exam paper text
    
    Args:
        exam_text: Full exam paper text
        
    Returns:
        List of individual questions
    """
    questions = []
    
    # Pattern 1: Questions starting with numbers (1., 2., Q1, etc.)
    pattern1 = r'(?:^|\n)\s*(?:Q\.?\s*)?(\d+)[\.\)]\s*([^\n]+(?:\n(?!\s*(?:Q\.?\s*)?\d+[\.\)]).*)*)'
    matches1 = re.finditer(pattern1, exam_text, re.MULTILINE | re.IGNORECASE)
    
    for match in matches1:
        question_text = match.group(2).strip()
        if len(question_text) > 10:  # Filter out very short matches
            questions.append(clean_text(question_text))
    
    # Pattern 2: Questions starting with letters (a), b), etc.)
    if len(questions) < 3:  # If few questions found, try alternative pattern
        pattern2 = r'(?:^|\n)\s*([a-z][\.\)])\s*([^\n]+)'
        matches2 = re.finditer(pattern2, exam_text, re.MULTILINE | re.IGNORECASE)
        
        for match in matches2:
            question_text = match.group(2).strip()
            if len(question_text) > 10:
                questions.append(clean_text(question_text))
    
    # Fallback: Split by double newlines if patterns don't work well
    if len(questions) < 3:
        chunks = exam_text.split('\n\n')
        questions = [clean_text(chunk) for chunk in chunks if len(chunk.strip()) > 20]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_questions = []
    for q in questions:
        if q not in seen and len(q) > 15:
            seen.add(q)
            unique_questions.append(q)
    
    return unique_questions[:50]  # Limit to 50 questions max

def validate_exam_paper(text: str) -> bool:
    """
    Validate that text looks like an exam paper
    
    Args:
        text: Exam paper text
        
    Returns:
        True if valid, False otherwise
    """
    if len(text) < 50:
        return False
    
    # Check for question indicators
    question_patterns = [
        r'\d+[\.\)]',  # Numbered questions
        r'Q\d+',        # Q1, Q2, etc.
        r'[Qq]uestion',  # Word "question"
        r'[Aa]nswer',    # Word "answer"
    ]
    
    matches = sum(1 for pattern in question_patterns if re.search(pattern, text))
    
    return matches >= 2

def validate_syllabus(text: str) -> bool:
    """
    Validate that text looks like a syllabus
    
    Args:
        text: Syllabus text
        
    Returns:
        True if valid, False otherwise
    """
    if len(text) < 50:
        return False
    
    # Check for syllabus indicators
    syllabus_patterns = [
        r'[Uu]nit',
        r'[Mm]odule',
        r'[Cc]hapter',
        r'[Ss]yllabus',
        r'[Cc]ourse',
        r'[Oo]bjective',
    ]
    
    matches = sum(1 for pattern in syllabus_patterns if re.search(pattern, text))
    
    return matches >= 2
