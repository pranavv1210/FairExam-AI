"""
Azure AI Language Service Integration (Using Azure OpenAI)
Handles key phrase extraction, topic extraction, and semantic matching
Now powered by Azure OpenAI GPT-4 instead of Azure Language service
"""

import os
import logging
from openai import AzureOpenAI
from typing import List, Dict, Any
import re
import json

logger = logging.getLogger(__name__)

class AzureLanguageService:
    """Service for text analysis using Azure OpenAI"""
    
    def __init__(self):
        # Use Azure OpenAI instead of Language service
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        if not self.endpoint or not self.api_key or not self.deployment:
            logger.warning("Azure OpenAI credentials not configured")
            self.client = None
        else:
            self.client = AzureOpenAI(
                azure_endpoint=self.endpoint,
                api_key=self.api_key,
                api_version="2024-08-01-preview"
            )
    
    def extract_topics_from_syllabus(self, syllabus_text: str) -> List[str]:
        """
        Extract key topics from syllabus using Azure OpenAI GPT-4
        
        Args:
            syllabus_text: Full syllabus text
            
        Returns:
            List of extracted topics/units
        """
        if not self.client:
            return self._fallback_topic_extraction(syllabus_text)
        
        try:
            prompt = f"""Extract the main topics, units, and concepts from this syllabus.
Return ONLY a JSON array of topic strings (10-15 topics maximum).

Syllabus:
{syllabus_text[:4000]}

Return format: ["Topic 1", "Topic 2", ...]"""

            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            
            result = response.choices[0].message.content.strip()
            
            # Parse JSON response
            if result.startswith("```json"):
                result = result.replace("```json", "").replace("```", "").strip()
            
            topics = json.loads(result)
            
            if isinstance(topics, list):
                return topics[:15]
            else:
                return self._fallback_topic_extraction(syllabus_text)
            
        except Exception as e:
            logger.error(f"Error in topic extraction: {e}")
            return self._fallback_topic_extraction(syllabus_text)
    
    def match_questions_to_topics(self, questions: List[str], topics: List[str]) -> Dict[str, Any]:
        """
        Match questions to syllabus topics using Azure OpenAI GPT-4
        
        Args:
            questions: List of question texts
            topics: List of syllabus topics
            
        Returns:
            Dict with matching results and coverage analysis
        """
        if not self.client:
            return self._fallback_topic_matching(questions, topics)
        
        try:
            # Match all questions in one API call for efficiency
            prompt = f"""Match each question to the most relevant syllabus topics.
Return ONLY a JSON object mapping question indices to arrays of matching topic names.

Topics: {json.dumps(topics)}

Questions:
{json.dumps([f"Q{i+1}: {q[:200]}" for i, q in enumerate(questions)])}

Return format: {{"0": ["Topic A", "Topic B"], "1": ["Topic C"], ...}}"""

            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content.strip()
            
            # Clean JSON markers if present
            if result.startswith("```json"):
                result = result.replace("```json", "").replace("```", "").strip()
            
            matches_data = json.loads(result)
            
            question_topic_map = []
            topic_coverage = {topic: 0 for topic in topics}
            
            for i, question in enumerate(questions):
                question_matches = matches_data.get(str(i), [])
                
                matched_topics = []
                for topic_name in question_matches:
                    if topic_name in topics:
                        matched_topics.append({
                            "topic": topic_name,
                            "confidence": 0.8
                        })
                        topic_coverage[topic_name] += 1
                
                # If no matches, use best fallback
                if not matched_topics:
                    matched_topics = [{"topic": "Unmatched", "confidence": 0}]
                
                question_topic_map.append({
                    "question": question[:100] + "..." if len(question) > 100 else question,
                    "matched_topics": matched_topics,
                    "best_match": matched_topics[0]["topic"]
                })
            
            # Calculate coverage statistics
            total_topics = len(topics)
            covered_topics = sum(1 for count in topic_coverage.values() if count > 0)
            coverage_percentage = (covered_topics / total_topics * 100) if total_topics > 0 else 0
            
            # Identify over-represented and ignored topics
            avg_questions_per_topic = len(questions) / total_topics if total_topics > 0 else 0
            over_represented = [topic for topic, count in topic_coverage.items() if count > avg_questions_per_topic * 1.5]
            ignored_topics = [topic for topic, count in topic_coverage.items() if count == 0]
            
            return {
                "question_topic_mapping": question_topic_map,
                "topic_coverage": topic_coverage,
                "coverage_percentage": round(coverage_percentage, 2),
                "covered_topics": covered_topics,
                "total_topics": total_topics,
                "over_represented": over_represented,
                "ignored_topics": ignored_topics
            }
            
        except Exception as e:
            logger.error(f"Error in topic matching: {e}")
            return self._fallback_topic_matching(questions, topics)
    
    def _fallback_topic_extraction(self, syllabus_text: str) -> List[str]:
        """Fallback topic extraction using simple text processing"""
        topics = []
        
        # Look for numbered sections (Unit 1, Module 1, etc.)
        unit_pattern = r'(?:Unit|Module|Chapter|Topic)\s+\d+[:\-\s]+([^\n\.]+)'
        matches = re.findall(unit_pattern, syllabus_text, re.IGNORECASE)
        topics.extend([m.strip() for m in matches])
        
        # Look for bullet points or headings
        lines = syllabus_text.split('\n')
        for line in lines:
            line = line.strip()
            if len(line) > 10 and len(line) < 100:
                # Heuristic: lines of medium length might be topics
                if line[0].isupper() or line.startswith('-') or line.startswith('•'):
                    cleaned = line.lstrip('-•').strip()
                    if cleaned:
                        topics.append(cleaned)
        
        # Remove duplicates and return
        unique_topics = list(set(topics))
        return unique_topics[:15] if unique_topics else ["General Topics"]
    
    def _fallback_topic_matching(self, questions: List[str], topics: List[str]) -> Dict[str, Any]:
        """Fallback topic matching using simple keyword overlap"""
        question_topic_map = []
        topic_coverage = {topic: 0 for topic in topics}
        
        for question in questions:
            question_words = set(question.lower().split())
            matches = []
            
            for topic in topics:
                topic_words = set(topic.lower().split())
                overlap = len(question_words.intersection(topic_words))
                
                if overlap > 0:
                    matches.append({
                        "topic": topic,
                        "confidence": min(overlap * 0.2, 1.0)
                    })
            
            matches.sort(key=lambda x: x["confidence"], reverse=True)
            best_match = matches[0] if matches else {"topic": "General", "confidence": 0}
            
            question_topic_map.append({
                "question": question[:100] + "..." if len(question) > 100 else question,
                "matched_topics": matches[:3] if matches else [best_match],
                "best_match": best_match["topic"]
            })
            
            if best_match["topic"] in topic_coverage:
                topic_coverage[best_match["topic"]] += 1
        
        total_topics = len(topics)
        covered_topics = sum(1 for count in topic_coverage.values() if count > 0)
        coverage_percentage = (covered_topics / total_topics * 100) if total_topics > 0 else 0
        
        avg_questions_per_topic = len(questions) / total_topics if total_topics > 0 else 0
        over_represented = [topic for topic, count in topic_coverage.items() if count > avg_questions_per_topic * 1.5]
        ignored_topics = [topic for topic, count in topic_coverage.items() if count == 0]
        
        return {
            "question_topic_mapping": question_topic_map,
            "topic_coverage": topic_coverage,
            "coverage_percentage": round(coverage_percentage, 2),
            "covered_topics": covered_topics,
            "total_topics": total_topics,
            "over_represented": over_represented,
            "ignored_topics": ignored_topics
        }
