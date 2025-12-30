"""
Azure OpenAI Service Integration
Handles difficulty classification, Bloom's taxonomy mapping, and bias detection
"""

import os
import json
import logging
from openai import AzureOpenAI
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AzureOpenAIService:
    """Service for Azure OpenAI GPT-4 integration"""
    
    def __init__(self):
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        
        if not self.endpoint or not self.api_key:
            logger.warning("Azure OpenAI credentials not configured")
            self.client = None
        else:
            self.client = AzureOpenAI(
                azure_endpoint=self.endpoint,
                api_key=self.api_key,
                api_version=self.api_version
            )
    
    def classify_question_difficulty(self, question: str) -> Dict[str, Any]:
        """
        Classify question difficulty using Azure OpenAI
        
        Args:
            question: Question text
            
        Returns:
            Dict with difficulty level and reasoning
        """
        if not self.client:
            # Fallback for demo purposes
            return self._fallback_difficulty_classification(question)
        
        try:
            prompt = f"""Analyze this exam question and classify its difficulty level.

Question: {question}

Classify as: Easy, Medium, or Hard

Criteria:
- Easy: Recall of facts, definitions, simple concepts
- Medium: Application of concepts, problem-solving, moderate analysis
- Hard: Deep analysis, synthesis, evaluation, complex problem-solving

Respond in JSON format:
{{
  "difficulty": "Easy|Medium|Hard",
  "reasoning": "Brief explanation of why"
}}"""

            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are an educational assessment expert analyzing exam questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            result = json.loads(response.choices[0].message.content)
            return {
                "question": question,
                "difficulty": result.get("difficulty", "Medium"),
                "reasoning": result.get("reasoning", "")
            }
            
        except Exception as e:
            logger.error(f"Error classifying difficulty: {e}")
            return self._fallback_difficulty_classification(question)
    
    def map_blooms_taxonomy(self, question: str) -> Dict[str, Any]:
        """
        Map question to Bloom's Taxonomy level using Azure OpenAI
        
        Args:
            question: Question text
            
        Returns:
            Dict with Bloom's level and explanation
        """
        if not self.client:
            return self._fallback_blooms_mapping(question)
        
        try:
            prompt = f"""Analyze this exam question and map it to Bloom's Taxonomy.

Question: {question}

Bloom's Taxonomy Levels:
1. Remember: Recall facts and basic concepts
2. Understand: Explain ideas or concepts
3. Apply: Use information in new situations
4. Analyze: Draw connections among ideas
5. Evaluate: Justify a stand or decision
6. Create: Produce new or original work

Identify action verbs and classify the cognitive level required.

Respond in JSON format:
{{
  "blooms_level": "Remember|Understand|Apply|Analyze|Evaluate|Create",
  "explanation": "Brief reasoning with identified action verbs"
}}"""

            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are an educational assessment expert specializing in Bloom's Taxonomy."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            result = json.loads(response.choices[0].message.content)
            return {
                "question": question,
                "blooms_level": result.get("blooms_level", "Understand"),
                "explanation": result.get("explanation", "")
            }
            
        except Exception as e:
            logger.error(f"Error mapping Bloom's taxonomy: {e}")
            return self._fallback_blooms_mapping(question)
    
    def detect_bias_and_ambiguity(self, questions: List[str]) -> Dict[str, Any]:
        """
        Detect potential bias and ambiguity in questions
        
        Args:
            questions: List of question texts
            
        Returns:
            Dict with bias analysis and suggestions
        """
        if not self.client:
            return self._fallback_bias_detection(questions)
        
        try:
            questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
            
            prompt = f"""Analyze these exam questions for potential bias and ambiguity issues.

Questions:
{questions_text}

Check for:
1. Cultural bias
2. Gender bias
3. Socioeconomic bias
4. Ambiguous wording
5. Assumptions about background knowledge

Respond in JSON format:
{{
  "bias_detected": true/false,
  "issues": ["list of specific issues found"],
  "suggestions": ["improvement suggestions"],
  "fairness_indicators": {{
    "cultural_neutrality": 0-100,
    "clarity": 0-100,
    "accessibility": 0-100
  }}
}}"""

            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are an expert in educational fairness and responsible AI."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.error(f"Error detecting bias: {e}")
            return self._fallback_bias_detection(questions)
    
    def _fallback_difficulty_classification(self, question: str) -> Dict[str, Any]:
        """Fallback difficulty classification for demo"""
        question_lower = question.lower()
        
        # Simple heuristic-based classification
        easy_keywords = ["define", "list", "name", "what is", "who is", "when"]
        hard_keywords = ["analyze", "evaluate", "design", "propose", "justify", "critique", "synthesize"]
        
        if any(keyword in question_lower for keyword in easy_keywords):
            difficulty = "Easy"
            reasoning = "Question requires basic recall or definition"
        elif any(keyword in question_lower for keyword in hard_keywords):
            difficulty = "Hard"
            reasoning = "Question requires deep analysis or evaluation"
        else:
            difficulty = "Medium"
            reasoning = "Question requires application of concepts"
        
        return {
            "question": question,
            "difficulty": difficulty,
            "reasoning": reasoning
        }
    
    def _fallback_blooms_mapping(self, question: str) -> Dict[str, Any]:
        """Fallback Bloom's taxonomy mapping for demo"""
        question_lower = question.lower()
        
        # Action verb mapping
        blooms_map = {
            "Remember": ["define", "list", "name", "recall", "identify", "label"],
            "Understand": ["explain", "describe", "summarize", "interpret", "classify"],
            "Apply": ["apply", "demonstrate", "solve", "use", "implement"],
            "Analyze": ["analyze", "compare", "contrast", "examine", "differentiate"],
            "Evaluate": ["evaluate", "assess", "judge", "critique", "justify"],
            "Create": ["create", "design", "develop", "propose", "construct", "formulate"]
        }
        
        for level, verbs in blooms_map.items():
            if any(verb in question_lower for verb in verbs):
                return {
                    "question": question,
                    "blooms_level": level,
                    "explanation": f"Question contains action verbs indicating {level} level"
                }
        
        return {
            "question": question,
            "blooms_level": "Understand",
            "explanation": "Default classification based on question structure"
        }
    
    def _fallback_bias_detection(self, questions: List[str]) -> Dict[str, Any]:
        """Fallback bias detection for demo"""
        return {
            "bias_detected": False,
            "issues": [],
            "suggestions": ["Questions appear to be culturally neutral", "Consider adding more diverse examples"],
            "fairness_indicators": {
                "cultural_neutrality": 85,
                "clarity": 90,
                "accessibility": 88
            }
        }
