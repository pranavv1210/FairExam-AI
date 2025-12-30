"""
Analysis API Routes
Handles exam paper analysis requests
"""

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import logging
from typing import List
from collections import Counter

from services.azure_openai import AzureOpenAIService
from services.azure_language import AzureLanguageService
from services.fairness_engine import FairnessEngine
from utils.pdf_parser import parse_document
from utils.text_cleaner import extract_questions, validate_exam_paper, validate_syllabus

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
openai_service = AzureOpenAIService()
language_service = AzureLanguageService()
fairness_engine = FairnessEngine()

@router.post("/analyze")
async def analyze_exam_paper(
    exam_paper: UploadFile = File(..., description="Exam paper PDF or TXT file"),
    syllabus: UploadFile = File(..., description="Syllabus PDF or TXT file")
):
    """
    Analyze exam paper for fairness and bias
    
    This endpoint:
    1. Extracts text from uploaded files
    2. Analyzes difficulty distribution using Azure OpenAI
    3. Maps questions to Bloom's Taxonomy using Azure OpenAI
    4. Extracts syllabus topics using Azure AI Language
    5. Matches questions to topics using Azure AI Language
    6. Calculates comprehensive fairness score
    7. Provides actionable suggestions
    
    Args:
        exam_paper: Uploaded exam paper file (PDF or TXT)
        syllabus: Uploaded syllabus file (PDF or TXT)
        
    Returns:
        Comprehensive analysis results with fairness score
    """
    
    try:
        logger.info(f"Starting analysis for exam: {exam_paper.filename}, syllabus: {syllabus.filename}")
        
        # Step 1: Extract text from files
        exam_bytes = await exam_paper.read()
        syllabus_bytes = await syllabus.read()
        
        exam_text = parse_document(exam_bytes, exam_paper.filename)
        syllabus_text = parse_document(syllabus_bytes, syllabus.filename)
        
        # Validate content
        if not validate_exam_paper(exam_text):
            raise HTTPException(status_code=400, detail="Uploaded file does not appear to be a valid exam paper")
        
        if not validate_syllabus(syllabus_text):
            raise HTTPException(status_code=400, detail="Uploaded file does not appear to be a valid syllabus")
        
        logger.info(f"Extracted exam text: {len(exam_text)} chars, syllabus: {len(syllabus_text)} chars")
        
        # Step 2: Extract individual questions
        questions = extract_questions(exam_text)
        
        if len(questions) < 3:
            raise HTTPException(
                status_code=400,
                detail="Could not extract sufficient questions from exam paper. Please ensure the file contains clearly numbered or formatted questions."
            )
        
        logger.info(f"Extracted {len(questions)} questions")
        
        # Step 3: Analyze difficulty for each question (Azure OpenAI)
        logger.info("Analyzing question difficulty...")
        difficulty_results = []
        for question in questions:
            result = openai_service.classify_question_difficulty(question)
            difficulty_results.append(result)
        
        # Aggregate difficulty distribution
        difficulty_counts = Counter([r["difficulty"] for r in difficulty_results])
        difficulty_analysis = {
            "distribution": dict(difficulty_counts),
            "total_questions": len(questions),
            "details": difficulty_results
        }
        
        # Step 4: Map questions to Bloom's Taxonomy (Azure OpenAI)
        logger.info("Mapping to Bloom's Taxonomy...")
        blooms_results = []
        for question in questions:
            result = openai_service.map_blooms_taxonomy(question)
            blooms_results.append(result)
        
        # Aggregate Bloom's distribution
        blooms_counts = Counter([r["blooms_level"] for r in blooms_results])
        blooms_analysis = {
            "distribution": dict(blooms_counts),
            "total_questions": len(questions),
            "details": blooms_results
        }
        
        # Step 5: Extract syllabus topics (Azure AI Language)
        logger.info("Extracting syllabus topics...")
        syllabus_topics = language_service.extract_topics_from_syllabus(syllabus_text)
        
        logger.info(f"Extracted {len(syllabus_topics)} topics from syllabus")
        
        # Step 6: Match questions to syllabus topics (Azure AI Language)
        logger.info("Matching questions to syllabus topics...")
        coverage_analysis = language_service.match_questions_to_topics(questions, syllabus_topics)
        
        # Step 7: Detect bias and ambiguity (Azure OpenAI)
        logger.info("Detecting bias and ambiguity...")
        bias_analysis = openai_service.detect_bias_and_ambiguity(questions)
        
        # Step 8: Calculate comprehensive fairness score
        logger.info("Calculating fairness score...")
        fairness_result = fairness_engine.calculate_fairness_score(
            difficulty_analysis,
            blooms_analysis,
            coverage_analysis
        )
        
        # Step 9: Compile complete analysis
        complete_analysis = {
            "fairness_score": fairness_result["fairness_score"],
            "interpretation": fairness_result["interpretation"],
            "component_scores": fairness_result["component_scores"],
            "suggestions": fairness_result["suggestions"],
            "difficulty_analysis": {
                "distribution": difficulty_analysis["distribution"],
                "total_questions": difficulty_analysis["total_questions"]
            },
            "blooms_analysis": {
                "distribution": blooms_analysis["distribution"],
                "total_questions": blooms_analysis["total_questions"]
            },
            "coverage_analysis": {
                "coverage_percentage": coverage_analysis["coverage_percentage"],
                "covered_topics": coverage_analysis["covered_topics"],
                "total_topics": coverage_analysis["total_topics"],
                "topic_coverage": coverage_analysis["topic_coverage"],
                "over_represented": coverage_analysis["over_represented"],
                "ignored_topics": coverage_analysis["ignored_topics"]
            },
            "bias_analysis": bias_analysis,
            "exam_metadata": {
                "total_questions": len(questions),
                "syllabus_topics": syllabus_topics,
                "exam_filename": exam_paper.filename,
                "syllabus_filename": syllabus.filename
            }
        }
        
        logger.info(f"Analysis complete. Fairness score: {fairness_result['fairness_score']}")
        
        return JSONResponse(content=complete_analysis)
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/test-azure-services")
async def test_azure_services():
    """
    Test endpoint to verify Azure service connectivity
    
    Returns:
        Status of Azure OpenAI and Azure AI Language services
    """
    results = {
        "azure_openai": {
            "configured": openai_service.client is not None,
            "status": "ready" if openai_service.client else "not configured"
        },
        "azure_language": {
            "configured": language_service.client is not None,
            "status": "ready" if language_service.client else "not configured"
        }
    }
    
    # Test Azure OpenAI with a simple query
    if openai_service.client:
        try:
            test_result = openai_service.classify_question_difficulty("Define machine learning")
            results["azure_openai"]["test_result"] = "success"
        except Exception as e:
            results["azure_openai"]["test_result"] = f"error: {str(e)}"
    
    # Test Azure AI Language with a simple query
    if language_service.client:
        try:
            test_topics = language_service.extract_topics_from_syllabus("Unit 1: Introduction to Computer Networks")
            results["azure_language"]["test_result"] = "success"
        except Exception as e:
            results["azure_language"]["test_result"] = f"error: {str(e)}"
    
    return JSONResponse(content=results)
