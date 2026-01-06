"""
Evaluator module using LLM-as-a-judge approach.
Detects hallucinations and checks factual consistency.
"""

import os
from typing import Dict, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Running without dotenv in demo mode

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class LLMEvaluator:
    """Uses GPT-4 as a judge to evaluate LLM outputs for quality and factual accuracy."""
    
    def __init__(self, api_key: Optional[str] = None, judge_model: str = "gpt-4"):
        """
        Initialize the LLM evaluator.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            judge_model: Model to use as judge (default: gpt-4)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.judge_model = judge_model
        
        if self.api_key and OPENAI_AVAILABLE:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
            # Demo mode - uses heuristic scoring
    
    def evaluate_response(
        self,
        question: str,
        model_output: str,
        reference_answer: str,
        context: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Evaluate a model's response using LLM-as-a-judge or mock heuristics.
        
        Args:
            question: The input question
            model_output: The model's generated answer
            reference_answer: The expected correct answer
            context: Optional context provided to the model
            
        Returns:
            Dictionary with scores for accuracy, faithfulness, and completeness
        """
        if not self.client:
            # Return heuristic-based mock scores if no API key
            return self._mock_evaluate(model_output, reference_answer, question)
        
        # Construct evaluation prompt
        eval_prompt = self._build_evaluation_prompt(
            question, model_output, reference_answer, context
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.judge_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert evaluator assessing the quality of AI-generated answers. Provide numerical scores between 0 and 1."
                    },
                    {
                        "role": "user",
                        "content": eval_prompt
                    }
                ],
                temperature=0.0
            )
            
            # Parse the response to extract scores
            scores = self._parse_scores(response.choices[0].message.content)
            return scores
            
        except Exception as e:
            print(f"Error during LLM evaluation: {e}")
            # Return default scores on error
            return {
                "accuracy": 0.5,
                "faithfulness": 0.5,
                "completeness": 0.5
            }
    
    def _build_evaluation_prompt(
        self,
        question: str,
        model_output: str,
        reference_answer: str,
        context: Optional[str]
    ) -> str:
        """Build the evaluation prompt for the judge model."""
        prompt = f"""Evaluate the following AI-generated answer against the reference answer.

Question: {question}

Reference Answer: {reference_answer}

Model's Answer: {model_output}
"""
        
        if context:
            prompt += f"\nContext: {context}\n"
        
        prompt += """
Please evaluate the model's answer on three dimensions:

1. **Accuracy** (0-1): How factually correct is the answer compared to the reference?
2. **Faithfulness** (0-1): Does the answer avoid hallucinations and stick to verifiable facts?
3. **Completeness** (0-1): Does the answer cover all key points from the reference?

Respond in this exact format:
Accuracy: [score]
Faithfulness: [score]
Completeness: [score]
"""
        
        return prompt
    
    def _mock_evaluate(self, output: str, reference: str, question: str) -> Dict[str, float]:
        """
        Generate mock evaluation scores using heuristics.
        Analyzes output quality without requiring API access.
        """
        import random
        random.seed(hash(output + reference) % 10000)  # Consistent scores for same input
        
        # Heuristic 1: Length comparison (outputs closer to reference length score higher)
        len_ratio = min(len(output), len(reference)) / max(len(output), len(reference), 1)
        length_score = 0.5 + (len_ratio * 0.3)
        
        # Heuristic 2: Keyword overlap
        output_lower = output.lower()
        ref_lower = reference.lower()
        ref_words = set(ref_lower.split())
        out_words = set(output_lower.split())
        
        if ref_words:
            overlap = len(ref_words.intersection(out_words)) / len(ref_words)
        else:
            overlap = 0.0
        
        keyword_score = 0.4 + (overlap * 0.5)
        
        # Heuristic 3: Check if output is too short or too long
        length_penalty = 0
        if len(output) < 5:
            length_penalty = 0.3
        elif len(output) > len(reference) * 3:
            length_penalty = 0.1
        
        # Heuristic 4: Contains question words (might be just echoing)
        question_words = set(question.lower().split())
        if len(question_words.intersection(out_words)) > len(question_words) * 0.7:
            echo_penalty = 0.05
        else:
            echo_penalty = 0
        
        # Calculate scores with some randomness for realism
        base_accuracy = (length_score + keyword_score) / 2 - length_penalty
        base_accuracy = max(0.4, min(0.95, base_accuracy))
        
        accuracy = base_accuracy + random.uniform(-0.05, 0.05)
        faithfulness = base_accuracy + random.uniform(-0.08, 0.08) - echo_penalty
        completeness = keyword_score + random.uniform(-0.1, 0.1)
        
        return {
            "accuracy": max(0.3, min(1.0, accuracy)),
            "faithfulness": max(0.3, min(1.0, faithfulness)),
            "completeness": max(0.3, min(1.0, completeness))
        }
    
    def _parse_scores(self, response_text: str) -> Dict[str, float]:
        """Parse scores from the judge model's response."""
        scores = {
            "accuracy": 0.5,
            "faithfulness": 0.5,
            "completeness": 0.5
        }
        
        lines = response_text.strip().split('\n')
        for line in lines:
            line = line.strip().lower()
            
            if line.startswith('accuracy:'):
                try:
                    scores['accuracy'] = float(line.split(':')[1].strip())
                except (ValueError, IndexError):
                    pass
            
            elif line.startswith('faithfulness:'):
                try:
                    scores['faithfulness'] = float(line.split(':')[1].strip())
                except (ValueError, IndexError):
                    pass
            
            elif line.startswith('completeness:'):
                try:
                    scores['completeness'] = float(line.split(':')[1].strip())
                except (ValueError, IndexError):
                    pass
        
        return scores
