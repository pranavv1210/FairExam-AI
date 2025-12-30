"""
Fairness Score Calculation Engine
Calculates comprehensive fairness score based on multiple factors
"""

import logging
from typing import Dict, List, Any
from collections import Counter

logger = logging.getLogger(__name__)

class FairnessEngine:
    """
    Core engine for calculating exam paper fairness score
    
    Fairness Score Formula:
    40% Difficulty Balance + 30% Bloom's Balance + 30% Syllabus Coverage
    """
    
    def calculate_fairness_score(
        self,
        difficulty_analysis: Dict[str, Any],
        blooms_analysis: Dict[str, Any],
        coverage_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive fairness score
        
        Args:
            difficulty_analysis: Results from difficulty classification
            blooms_analysis: Results from Bloom's taxonomy mapping
            coverage_analysis: Results from syllabus coverage analysis
            
        Returns:
            Complete fairness analysis with score and breakdown
        """
        
        # Calculate individual component scores
        difficulty_score = self._calculate_difficulty_balance_score(difficulty_analysis)
        blooms_score = self._calculate_blooms_balance_score(blooms_analysis)
        coverage_score = self._calculate_coverage_score(coverage_analysis)
        
        # Weighted final score
        final_score = round(
            (difficulty_score * 0.40) +
            (blooms_score * 0.30) +
            (coverage_score * 0.30)
        , 2)
        
        # Generate interpretation
        interpretation = self._interpret_score(final_score)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(
            difficulty_analysis,
            blooms_analysis,
            coverage_analysis,
            difficulty_score,
            blooms_score,
            coverage_score
        )
        
        return {
            "fairness_score": final_score,
            "interpretation": interpretation,
            "component_scores": {
                "difficulty_balance": {
                    "score": difficulty_score,
                    "weight": 40,
                    "weighted_contribution": round(difficulty_score * 0.40, 2)
                },
                "blooms_balance": {
                    "score": blooms_score,
                    "weight": 30,
                    "weighted_contribution": round(blooms_score * 0.30, 2)
                },
                "syllabus_coverage": {
                    "score": coverage_score,
                    "weight": 30,
                    "weighted_contribution": round(coverage_score * 0.30, 2)
                }
            },
            "suggestions": suggestions,
            "detailed_analysis": {
                "difficulty_distribution": difficulty_analysis,
                "blooms_distribution": blooms_analysis,
                "coverage_details": coverage_analysis
            }
        }
    
    def _calculate_difficulty_balance_score(self, difficulty_analysis: Dict[str, Any]) -> float:
        """
        Calculate difficulty balance score (0-100)
        
        Ideal distribution: 30% Easy, 50% Medium, 20% Hard
        """
        distribution = difficulty_analysis.get("distribution", {})
        total = difficulty_analysis.get("total_questions", 0)
        
        if total == 0:
            return 0.0
        
        # Get percentages
        easy_pct = (distribution.get("Easy", 0) / total) * 100
        medium_pct = (distribution.get("Medium", 0) / total) * 100
        hard_pct = (distribution.get("Hard", 0) / total) * 100
        
        # Ideal targets
        ideal_easy = 30
        ideal_medium = 50
        ideal_hard = 20
        
        # Calculate deviation from ideal
        easy_deviation = abs(easy_pct - ideal_easy)
        medium_deviation = abs(medium_pct - ideal_medium)
        hard_deviation = abs(hard_pct - ideal_hard)
        
        # Average deviation (lower is better)
        avg_deviation = (easy_deviation + medium_deviation + hard_deviation) / 3
        
        # Convert to score (0-100, where lower deviation = higher score)
        score = max(0, 100 - (avg_deviation * 2))
        
        return round(score, 2)
    
    def _calculate_blooms_balance_score(self, blooms_analysis: Dict[str, Any]) -> float:
        """
        Calculate Bloom's taxonomy balance score (0-100)
        
        Good balance means questions across multiple cognitive levels
        """
        distribution = blooms_analysis.get("distribution", {})
        total = blooms_analysis.get("total_questions", 0)
        
        if total == 0:
            return 0.0
        
        # Get counts for each level
        levels = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
        level_counts = {level: distribution.get(level, 0) for level in levels}
        
        # Number of levels represented
        levels_represented = sum(1 for count in level_counts.values() if count > 0)
        
        # Ideal: Questions should span at least 4 different levels
        representation_score = (levels_represented / 6) * 100
        
        # Calculate balance (avoid over-concentration in one level)
        percentages = [(count / total) * 100 for count in level_counts.values()]
        max_concentration = max(percentages) if percentages else 0
        
        # Penalize if one level has > 50% of questions
        concentration_penalty = max(0, (max_concentration - 50) * 2)
        
        # Final score
        score = max(0, representation_score - concentration_penalty)
        
        return round(score, 2)
    
    def _calculate_coverage_score(self, coverage_analysis: Dict[str, Any]) -> float:
        """
        Calculate syllabus coverage score (0-100)
        
        Based on:
        - Percentage of topics covered
        - Balance across topics
        - No major gaps
        """
        coverage_pct = coverage_analysis.get("coverage_percentage", 0)
        over_represented = coverage_analysis.get("over_represented", [])
        ignored_topics = coverage_analysis.get("ignored_topics", [])
        total_topics = coverage_analysis.get("total_topics", 1)
        
        # Base score from coverage percentage
        base_score = coverage_pct
        
        # Penalty for ignored topics
        ignored_penalty = (len(ignored_topics) / total_topics) * 30
        
        # Penalty for over-representation
        over_rep_penalty = (len(over_represented) / total_topics) * 20
        
        # Final score
        score = max(0, base_score - ignored_penalty - over_rep_penalty)
        
        return round(score, 2)
    
    def _interpret_score(self, score: float) -> str:
        """Generate human-readable interpretation of fairness score"""
        if score >= 85:
            return "Excellent - This exam paper demonstrates strong fairness characteristics with well-balanced difficulty, comprehensive cognitive level coverage, and appropriate syllabus distribution."
        elif score >= 70:
            return "Good - This exam paper shows good fairness with minor areas for improvement in balance and coverage."
        elif score >= 55:
            return "Fair - This exam paper is acceptable but has noticeable imbalances that could affect student outcomes."
        elif score >= 40:
            return "Needs Improvement - This exam paper has significant fairness issues that should be addressed before use."
        else:
            return "Poor - This exam paper requires substantial revision to meet fairness standards."
    
    def _generate_suggestions(
        self,
        difficulty_analysis: Dict[str, Any],
        blooms_analysis: Dict[str, Any],
        coverage_analysis: Dict[str, Any],
        difficulty_score: float,
        blooms_score: float,
        coverage_score: float
    ) -> List[str]:
        """Generate actionable improvement suggestions"""
        suggestions = []
        
        # Difficulty suggestions
        if difficulty_score < 70:
            distribution = difficulty_analysis.get("distribution", {})
            total = difficulty_analysis.get("total_questions", 0)
            
            if total > 0:
                easy_pct = (distribution.get("Easy", 0) / total) * 100
                medium_pct = (distribution.get("Medium", 0) / total) * 100
                hard_pct = (distribution.get("Hard", 0) / total) * 100
                
                if easy_pct > 40:
                    suggestions.append("⚠️ Too many easy questions. Consider replacing some with medium-difficulty questions.")
                elif easy_pct < 20:
                    suggestions.append("⚠️ Add more easy questions to ensure accessibility for all students.")
                
                if medium_pct < 40:
                    suggestions.append("⚠️ Increase medium-difficulty questions to better assess core understanding.")
                
                if hard_pct > 30:
                    suggestions.append("⚠️ Too many hard questions may disadvantage students. Consider reducing complexity.")
                elif hard_pct < 10:
                    suggestions.append("⚠️ Add challenging questions to differentiate high-performing students.")
        
        # Bloom's taxonomy suggestions
        if blooms_score < 70:
            distribution = blooms_analysis.get("distribution", {})
            
            if distribution.get("Remember", 0) + distribution.get("Understand", 0) > len(distribution) * 0.6:
                suggestions.append("⚠️ Too many lower-order thinking questions. Add more analysis and application questions.")
            
            if distribution.get("Analyze", 0) + distribution.get("Evaluate", 0) + distribution.get("Create", 0) == 0:
                suggestions.append("⚠️ No higher-order thinking questions detected. Include questions requiring analysis or evaluation.")
        
        # Coverage suggestions
        if coverage_score < 70:
            ignored = coverage_analysis.get("ignored_topics", [])
            over_rep = coverage_analysis.get("over_represented", [])
            
            if ignored:
                suggestions.append(f"⚠️ {len(ignored)} syllabus topic(s) not covered: {', '.join(ignored[:3])}{'...' if len(ignored) > 3 else ''}")
            
            if over_rep:
                suggestions.append(f"⚠️ Over-emphasis on: {', '.join(over_rep[:3])}. Distribute questions more evenly.")
            
            if coverage_analysis.get("coverage_percentage", 0) < 60:
                suggestions.append("⚠️ Less than 60% of syllabus covered. Add questions for missing topics.")
        
        # Positive reinforcement
        if not suggestions:
            suggestions.append("✅ Exam paper shows excellent balance across all fairness dimensions.")
        
        return suggestions
