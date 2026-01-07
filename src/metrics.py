"""
Metrics module for evaluating LLM outputs.
Provides semantic similarity, exact match, and token overlap metrics.
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from typing import List, Dict


class MetricsCalculator:
    """Calculates various metrics for comparing LLM outputs with references."""
    
    def __init__(self):
        """Initialize the metrics calculator with lazy model loading."""
        self._model = None  # Lazy load to improve startup time
    
    @property
    def model(self):
        """Lazy-load the sentence transformer model on first use."""
        if self._model is None:
            # Using a lightweight model for fast semantic similarity
            self._model = SentenceTransformer('all-MiniLM-L6-v2')
        return self._model

    
    def semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts using sentence embeddings.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        embeddings = self.model.encode([text1, text2])
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        return float(similarity)
    
    def exact_match(self, predicted: str, reference: str) -> float:
        """
        Check if predicted text exactly matches reference (case-insensitive).
        
        Args:
            predicted: Model output
            reference: Expected output
            
        Returns:
            1.0 if exact match, 0.0 otherwise
        """
        return 1.0 if predicted.strip().lower() == reference.strip().lower() else 0.0
    
    def token_overlap_f1(self, predicted: str, reference: str) -> float:
        """
        Calculate F1 score based on token overlap.
        
        Args:
            predicted: Model output
            reference: Expected output
            
        Returns:
            F1 score between 0 and 1
        """
        pred_tokens = set(predicted.lower().split())
        ref_tokens = set(reference.lower().split())
        
        if len(pred_tokens) == 0 or len(ref_tokens) == 0:
            return 0.0
        
        common = pred_tokens.intersection(ref_tokens)
        
        if len(common) == 0:
            return 0.0
        
        precision = len(common) / len(pred_tokens)
        recall = len(common) / len(ref_tokens)
        
        f1 = 2 * (precision * recall) / (precision + recall)
        return f1
    
    def aggregate_scores(self, scores: List[Dict[str, float]]) -> Dict[str, float]:
        """
        Aggregate multiple evaluation scores into summary statistics.
        
        Args:
            scores: List of score dictionaries
            
        Returns:
            Dictionary with mean, min, max for each metric
        """
        if not scores:
            return {}
        
        # Get all metric keys
        metric_keys = set()
        for score in scores:
            metric_keys.update(score.keys())
        
        aggregated = {}
        for key in metric_keys:
            values = [s.get(key, 0.0) for s in scores]
            aggregated[f"{key}_mean"] = np.mean(values)
            aggregated[f"{key}_min"] = np.min(values)
            aggregated[f"{key}_max"] = np.max(values)
        
        return aggregated


# Convenience functions for standalone usage
_calculator = None

def get_calculator() -> MetricsCalculator:
    """Get or create singleton metrics calculator."""
    global _calculator
    if _calculator is None:
        _calculator = MetricsCalculator()
    return _calculator


def semantic_similarity(text1: str, text2: str) -> float:
    """Calculate semantic similarity between two texts."""
    return get_calculator().semantic_similarity(text1, text2)


def exact_match(predicted: str, reference: str) -> float:
    """Check for exact match between predicted and reference."""
    return get_calculator().exact_match(predicted, reference)


def token_overlap_f1(predicted: str, reference: str) -> float:
    """Calculate token overlap F1 score."""
    return get_calculator().token_overlap_f1(predicted, reference)
