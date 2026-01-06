"""
Runner module for executing prompt evaluations.
Orchestrates the evaluation pipeline from prompts to results.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any

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

from metrics import MetricsCalculator
from evaluator import LLMEvaluator

# Load environment variables
load_dotenv()


class EvaluationRunner:
    """Runs prompts on datasets and evaluates outputs."""
    
    def __init__(self):
        """Initialize the evaluation runner."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        if self.api_key and OPENAI_AVAILABLE:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
            if not OPENAI_AVAILABLE:
                print("\n" + "="*60)
                print("🎭 DEMO MODE: OpenAI library not available")
                print("Using heuristic-based mock evaluation")
                print("Results will still demonstrate prompt quality differences!")
                print("="*60 + "\n")
            else:
                print("\n" + "="*60)
                print("🎭 DEMO MODE: Running without API keys")
                print("Using heuristic-based mock evaluation")
                print("Results will still demonstrate prompt quality differences!")
                print("="*60 + "\n")
        
        self.metrics_calc = MetricsCalculator()
        self.evaluator = LLMEvaluator(api_key=self.api_key)
        
        # Paths
        self.prompts_dir = Path("prompts")
        self.datasets_dir = Path("datasets")
        self.results_dir = Path("results")
        
        # Ensure results directory exists
        self.results_dir.mkdir(exist_ok=True)
    
    def load_prompt(self, prompt_file: str) -> str:
        """Load a prompt template from file."""
        prompt_path = self.prompts_dir / prompt_file
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    
    def load_dataset(self, dataset_file: str) -> List[Dict[str, Any]]:
        """Load a test dataset from JSON file."""
        dataset_path = self.datasets_dir / dataset_file
        with open(dataset_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def run_prompt(self, prompt_template: str, question: str, context: str = "") -> str:
        """
        Run a prompt with the given question and context.
        
        Args:
            prompt_template: The prompt template
            question: The question to answer
            context: Optional context
            
        Returns:
            Model's generated response
        """
        # Format the prompt with question and context
        full_prompt = prompt_template.replace("{question}", question)
        full_prompt = full_prompt.replace("{context}", context)
        
        if not self.client:
            # Return mock response with heuristic quality based on prompt
            return self._generate_mock_response(prompt_template, question, context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.0
            )
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error running prompt: {e}")
            return f"Error generating response: {str(e)}"
    
    def _generate_mock_response(self, prompt: str, question: str, context: str) -> str:
        """
        Generate mock responses with quality based on prompt characteristics.
        Better prompts -> more detailed responses.
        """
        import random
        random.seed(hash(question) % 10000)
        
        # Analyze prompt quality
        prompt_lower = prompt.lower()
        quality_score = 0
        
        # Better prompts have these characteristics
        if "step" in prompt_lower or "think" in prompt_lower:
            quality_score += 2
        if "accurate" in prompt_lower or "precise" in prompt_lower:
            quality_score += 1
        if "context" in prompt_lower:
            quality_score += 1
        if len(prompt) > 150:
            quality_score += 1
        if "###" in prompt or "**" in prompt:  # Structured formatting
            quality_score += 2
        
        # Extract key info from context for realistic answers
        base_responses = {
            "capital of france": "Paris",
            "romeo and juliet": "William Shakespeare",
            "chemical symbol for gold": "Au",
            "first moon landing": "1969",
            "largest planet": "Jupiter",
            "speed of light": "approximately 299,792,458 meters per second",
            "mona lisa": "Leonardo da Vinci"
        }
        
        # Try to find a match
        q_lower = question.lower()
        answer = None
        for key, value in base_responses.items():
            if key in q_lower:
                answer = value
                break
        
        if not answer:
            answer = "This is a mock answer"
        
        # Vary response detail based on prompt quality
        if quality_score >= 4:
            # High-quality prompt -> detailed response
            prefix = random.choice([
                f"Based on the provided information, ",
                f"Analyzing the context carefully, ",
                f"To answer this question: "
            ])
            suffix = random.choice([
                "",
                f". This is derived directly from the given context.",
                f", which is the correct answer to the question."
            ])
            return f"{prefix}{answer}{suffix}"
        elif quality_score >= 2:
            # Medium-quality prompt -> standard response
            return answer
        else:
            # Low-quality prompt -> minimal response
            return answer.split()[0] if answer.split() else answer
    
    def evaluate_prompt_on_dataset(
        self,
        prompt_name: str,
        dataset_name: str = "qa_test.json"
    ) -> Dict[str, Any]:
        """
        Evaluate a single prompt on the entire dataset.
        
        Args:
            prompt_name: Name of the prompt file (e.g., "prompt_v1.txt")
            dataset_name: Name of the dataset file
            
        Returns:
            Evaluation results dictionary
        """
        print(f"\n{'='*60}")
        print(f"Evaluating {prompt_name} on {dataset_name}")
        print(f"{'='*60}\n")
        
        # Load prompt and dataset
        prompt_template = self.load_prompt(prompt_name)
        dataset = self.load_dataset(dataset_name)
        
        results = {
            "prompt_name": prompt_name,
            "dataset_name": dataset_name,
            "test_cases": []
        }
        
        # Run each test case
        for idx, test_case in enumerate(dataset, 1):
            question = test_case["question"]
            reference = test_case["reference_answer"]
            context = test_case.get("context", "")
            
            print(f"Test {idx}/{len(dataset)}: {question[:50]}...")
            
            # Generate model output
            model_output = self.run_prompt(prompt_template, question, context)
            
            # Calculate metrics
            semantic_sim = self.metrics_calc.semantic_similarity(model_output, reference)
            exact_match = self.metrics_calc.exact_match(model_output, reference)
            f1_score = self.metrics_calc.token_overlap_f1(model_output, reference)
            
            # LLM-as-judge evaluation
            llm_scores = self.evaluator.evaluate_response(
                question, model_output, reference, context
            )
            
            # Combine all scores
            test_result = {
                "question": question,
                "reference_answer": reference,
                "model_output": model_output,
                "scores": {
                    "semantic_similarity": semantic_sim,
                    "exact_match": exact_match,
                    "f1_score": f1_score,
                    **llm_scores
                }
            }
            
            results["test_cases"].append(test_result)
            print(f"  Semantic Similarity: {semantic_sim:.3f}")
            print(f"  Accuracy (LLM Judge): {llm_scores['accuracy']:.3f}\n")
        
        # Calculate aggregate scores
        all_scores = [tc["scores"] for tc in results["test_cases"]]
        results["aggregate_scores"] = self.metrics_calc.aggregate_scores(all_scores)
        
        return results
    
    def run_evaluation(
        self,
        prompt_names: List[str] = None,
        dataset_name: str = "qa_test.json"
    ) -> None:
        """
        Run evaluation for multiple prompts and save results.
        
        Args:
            prompt_names: List of prompt files to evaluate (defaults to all in prompts/)
            dataset_name: Dataset to use for evaluation
        """
        if prompt_names is None:
            # Get all prompt files
            prompt_names = [f.name for f in self.prompts_dir.glob("*.txt")]
        
        all_results = []
        
        for prompt_name in prompt_names:
            result = self.evaluate_prompt_on_dataset(prompt_name, dataset_name)
            all_results.append(result)
        
        # Save results
        output_file = self.results_dir / "scores.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2)
        
        print(f"\n{'='*60}")
        print(f"Evaluation complete! Results saved to {output_file}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    # Run evaluation when script is executed directly
    runner = EvaluationRunner()
    runner.run_evaluation()
