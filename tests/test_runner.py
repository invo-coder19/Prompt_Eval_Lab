"""
Unit tests for the runner module.
"""

import pytest
import json
from pathlib import Path
from runner import EvaluationRunner


class TestEvaluationRunner:
    """Test cases for EvaluationRunner class."""
    
    @pytest.fixture
    def runner(self):
        """Create an EvaluationRunner instance."""
        return EvaluationRunner()
    
    def test_initialization(self, runner):
        """Test runner initializes correctly."""
        assert runner is not None
        assert runner.evaluator is not None
        assert runner.metrics is not None
    
    def test_load_prompt(self, runner, tmp_path):
        """Test loading prompt from file."""
        # Create temporary prompt file
        prompt_file = tmp_path / "test_prompt.txt"
        prompt_content = "Answer: {question}"
        prompt_file.write_text(prompt_content)
        
        loaded = runner.load_prompt(str(prompt_file))
        assert loaded == prompt_content
    
    def test_load_dataset(self, runner, tmp_path, sample_dataset):
        """Test loading dataset from JSON file."""
        # Create temporary dataset file
        dataset_file = tmp_path / "test_dataset.json"
        dataset_file.write_text(json.dumps(sample_dataset))
        
        loaded = runner.load_dataset(str(dataset_file))
        assert len(loaded) == len(sample_dataset)
        assert loaded[0]["question"] == sample_dataset[0]["question"]
    
    def test_generate_mock_response_quality_tiers(self, runner):
        """Test mock responses vary by prompt quality."""
        question = "What is the capital of France?"
        context = "France is in Western Europe. Paris is its capital."
        
        # Simple prompt
        simple_prompt = "{question}"
        simple_response = runner._generate_mock_response(
            simple_prompt, question, context
        )
        
        # Complex prompt with instructions
        complex_prompt = """### Instructions:
Think step-by-step and provide an accurate answer.

Question: {question}
Context: {context}"""
        complex_response = runner._generate_mock_response(
            complex_prompt, question, context
        )
        
        # Complex response should be longer/more detailed
        assert len(complex_response) >= len(simple_response)
    
    def test_generate_mock_response_contains_answer(self, runner):
        """Test mock response contains expected answer."""
        question = "What is the capital of France?"
        context = ""
        prompt = "{question}"
        
        response = runner._generate_mock_response(prompt, question, context)
        
        # Should contain "Paris" somewhere
        assert "Paris" in response or "paris" in response.lower()
