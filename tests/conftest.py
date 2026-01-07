"""
Pytest configuration and shared fixtures.
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


@pytest.fixture
def sample_question():
    """Sample test question."""
    return "What is the capital of France?"


@pytest.fixture
def sample_reference():
    """Sample reference answer."""
    return "Paris"


@pytest.fixture
def sample_context():
    """Sample context."""
    return "France is a country in Western Europe. Its capital and largest city is Paris."


@pytest.fixture
def sample_output_good():
    """Sample good model output."""
    return "Paris is the capital of France."


@pytest.fixture
def sample_output_bad():
    """Sample poor model output."""
    return "I don't know."


@pytest.fixture
def sample_prompt_template():
    """Sample prompt template."""
    return """Answer the question based on the context.

Context: {context}
Question: {question}

Answer:"""


@pytest.fixture
def sample_dataset():
    """Sample test dataset."""
    return [
        {
            "id": 1,
            "question": "What is the capital of France?",
            "reference_answer": "Paris",
            "context": "France is a country in Western Europe. Its capital is Paris."
        },
        {
            "id": 2,
            "question": "Who wrote Romeo and Juliet?",
            "reference_answer": "William Shakespeare",
            "context": "Romeo and Juliet is a tragedy written by William Shakespeare."
        }
    ]
