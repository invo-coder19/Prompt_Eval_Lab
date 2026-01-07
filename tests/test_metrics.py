"""
Unit tests for the metrics module.
"""

import pytest
from metrics import MetricsCalculator


class TestMetricsCalculator:
    """Test cases for MetricsCalculator class."""
    
    @pytest.fixture
    def calculator(self):
        """Create a MetricsCalculator instance."""
        return MetricsCalculator()
    
    def test_initialization(self, calculator):
        """Test calculator initializes correctly."""
        assert calculator.model is not None
    
    def test_exact_match_identical(self, calculator):
        """Test exact match with identical texts."""
        text1 = "Paris is the capital"
        text2 = "Paris is the capital"
        
        score = calculator.exact_match(text1, text2)
        assert score == 1.0
    
    def test_exact_match_case_insensitive(self, calculator):
        """Test exact match is case insensitive."""
        text1 = "Paris"
        text2 = "paris"
        
        score = calculator.exact_match(text1, text2)
        assert score == 1.0
    
    def test_exact_match_with_whitespace(self, calculator):
        """Test exact match trims whitespace."""
        text1 = "  Paris  "
        text2 = "Paris"
        
        score = calculator.exact_match(text1, text2)
        assert score == 1.0
    
    def test_exact_match_different(self, calculator):
        """Test exact match with different texts."""
        text1 = "Paris"
        text2 = "London"
        
        score = calculator.exact_match(text1, text2)
        assert score == 0.0
    
    def test_token_overlap_f1_identical(self, calculator):
        """Test F1 with identical texts."""
        text1 = "Paris is the capital of France"
        text2 = "Paris is the capital of France"
        
        score = calculator.token_overlap_f1(text1, text2)
        assert score == 1.0
    
    def test_token_overlap_f1_partial_overlap(self, calculator):
        """Test F1 with partial overlap."""
        text1 = "Paris is the capital"
        text2 = "The capital city is Paris"
        
        score = calculator.token_overlap_f1(text1, text2)
        assert 0.0 < score < 1.0  # Should have some overlap
    
    def test_token_overlap_f1_no_overlap(self, calculator):
        """Test F1 with no overlap."""
        text1 = "Paris France"
        text2 = "London England"
        
        score = calculator.token_overlap_f1(text1, text2)
        assert score == 0.0
    
    def test_token_overlap_f1_empty_strings(self, calculator):
        """Test F1 with empty strings."""
        score = calculator.token_overlap_f1("", "Paris")
        assert score == 0.0
        
        score = calculator.token_overlap_f1("Paris", "")
        assert score == 0.0
    
    def test_semantic_similarity_identical(self, calculator):
        """Test semantic similarity with identical texts."""
        text1 = "Paris is the capital of France"
        text2 = "Paris is the capital of France"
        
        score = calculator.semantic_similarity(text1, text2)
        assert score >= 0.95  # Should be very high
    
    def test_semantic_similarity_similar_meaning(self, calculator):
        """Test semantic similarity with similar meaning."""
        text1 = "The capital of France is Paris"
        text2 = "Paris is France's capital city"
        
        score = calculator.semantic_similarity(text1, text2)
        assert score > 0.7  # Should be high
    
    def test_semantic_similarity_different_meaning(self, calculator):
        """Test semantic similarity with different meaning."""
        text1 = "Paris is the capital of France"
        text2 = "Tokyo is a large city in Japan"
        
        score = calculator.semantic_similarity(text1, text2)
        assert score < 0.5  # Should be lower
    
    def test_aggregate_scores_empty(self, calculator):
        """Test aggregate with empty list."""
        scores = calculator.aggregate_scores([])
        assert scores == {}
    
    def test_aggregate_scores_single(self, calculator):
        """Test aggregate with single score dict."""
        score_list = [
            {
                "accuracy": 0.8,
                "faithfulness": 0.7
            }
        ]
        
        aggregated = calculator.aggregate_scores(score_list)
        
        assert aggregated["accuracy_mean"] == 0.8
        assert aggregated["accuracy_min"] == 0.8
        assert aggregated["accuracy_max"] == 0.8
        assert aggregated["faithfulness_mean"] == 0.7
    
    def test_aggregate_scores_multiple(self, calculator):
        """Test aggregate with multiple score dicts."""
        score_list = [
            {"accuracy": 0.8, "faithfulness": 0.7},
            {"accuracy": 0.9, "faithfulness": 0.8},
            {"accuracy": 0.7, "faithfulness": 0.6}
        ]
        
        aggregated = calculator.aggregate_scores(score_list)
        
        assert aggregated["accuracy_mean"] == 0.8
        assert aggregated["accuracy_min"] == 0.7
        assert aggregated["accuracy_max"] == 0.9
        assert aggregated["faithfulness_mean"] == pytest.approx(0.7, 0.01)
        assert aggregated["faithfulness_min"] == 0.6
        assert aggregated["faithfulness_max"] == 0.8
