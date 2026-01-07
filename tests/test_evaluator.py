"""
Unit tests for the evaluator module.
"""

import pytest
from evaluator import LLMEvaluator


class TestLLMEvaluator:
    """Test cases for LLMEvaluator class."""
    
    def test_initialization_without_api_key(self):
        """Test evaluator initializes in demo mode without API key."""
        evaluator = LLMEvaluator(api_key=None)
        assert evaluator.client is None
        assert evaluator.api_key is None
    
    def test_initialization_with_api_key(self):
        """Test evaluator initializes with API key."""
        evaluator = LLMEvaluator(api_key="test_key")
        assert evaluator.api_key == "test_key"
    
    def test_mock_evaluate_returns_scores(
        self, 
        sample_question, 
        sample_output_good, 
        sample_reference
    ):
        """Test mock evaluation returns valid scores."""
        evaluator = LLMEvaluator(api_key=None)
        scores = evaluator._mock_evaluate(
            sample_output_good,
            sample_reference,
            sample_question
        )
        
        assert isinstance(scores, dict)
        assert 'accuracy' in scores
        assert 'faithfulness' in scores
        assert 'completeness' in scores
        
        # Scores should be between 0 and 1
        for key, value in scores.items():
            assert 0.0 <= value <= 1.0
    
    def test_mock_evaluate_good_vs_bad_output(
        self, 
        sample_question,
        sample_reference,
        sample_output_good,
        sample_output_bad
    ):
        """Test that good outputs score higher than bad outputs."""
        evaluator = LLMEvaluator(api_key=None)
        
        good_scores = evaluator._mock_evaluate(
            sample_output_good,
            sample_reference,
            sample_question
        )
        
        bad_scores = evaluator._mock_evaluate(
            sample_output_bad,
            sample_reference,
            sample_question
        )
        
        # Good output should score higher
        assert good_scores['accuracy'] > bad_scores['accuracy']
        assert good_scores['completeness'] > bad_scores['completeness']
    
    def test_evaluate_response_without_api_key(
        self,
        sample_question,
        sample_output_good,
        sample_reference,
        sample_context
    ):
        """Test evaluate_response falls back to mock when no API key."""
        evaluator = LLMEvaluator(api_key=None)
        scores = evaluator.evaluate_response(
            sample_question,
            sample_output_good,
            sample_reference,
            sample_context
        )
        
        assert isinstance(scores, dict)
        assert 'accuracy' in scores
    
    def test_parse_scores_valid_format(self):
        """Test parsing scores from judge response."""
        evaluator = LLMEvaluator(api_key=None)
        response_text = """
Accuracy: 0.95
Faithfulness: 0.90
Completeness: 0.85
        """
        
        scores = evaluator._parse_scores(response_text)
        
        assert scores['accuracy'] == 0.95
        assert scores['faithfulness'] == 0.90
        assert scores['completeness'] == 0.85
    
    def test_parse_scores_invalid_format(self):
        """Test parsing scores handles invalid format gracefully."""
        evaluator = LLMEvaluator(api_key=None)
        response_text = "Random text without scores"
        
        scores = evaluator._parse_scores(response_text)
        
        # Should return default scores
        assert scores['accuracy'] == 0.5
        assert scores['faithfulness'] == 0.5
        assert scores['completeness'] == 0.5
    
    def test_build_evaluation_prompt(
        self,
        sample_question,
        sample_output_good,
        sample_reference,
        sample_context
    ):
        """Test evaluation prompt building."""
        evaluator = LLMEvaluator(api_key=None)
        prompt = evaluator._build_evaluation_prompt(
            sample_question,
            sample_output_good,
            sample_reference,
            sample_context
        )
        
        assert isinstance(prompt, str)
        assert sample_question in prompt
        assert sample_output_good in prompt
        assert sample_reference in prompt
        assert sample_context in prompt
        assert "Accuracy" in prompt
        assert "Faithfulness" in prompt
        assert "Completeness" in prompt
