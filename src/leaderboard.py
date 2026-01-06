"""
Leaderboard module for ranking and comparing prompt performance.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from tabulate import tabulate


class Leaderboard:
    """Generates leaderboards from evaluation results."""
    
    def __init__(self, results_file: str = "results/scores.json"):
        """
        Initialize the leaderboard.
        
        Args:
            results_file: Path to the evaluation results JSON
        """
        self.results_file = Path(results_file)
        self.results = self._load_results()
    
    def _load_results(self) -> List[Dict[str, Any]]:
        """Load evaluation results from JSON file."""
        if not self.results_file.exists():
            print(f"Warning: Results file {self.results_file} not found.")
            return []
        
        with open(self.results_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_leaderboard_data(self) -> List[Dict[str, Any]]:
        """
        Get leaderboard data sorted by overall score.
        
        Returns:
            List of prompt results with rankings
        """
        leaderboard = []
        
        for result in self.results:
            prompt_name = result["prompt_name"]
            agg_scores = result.get("aggregate_scores", {})
            
            # Calculate overall score (weighted average of key metrics)
            overall_score = (
                agg_scores.get("semantic_similarity_mean", 0) * 0.3 +
                agg_scores.get("accuracy_mean", 0) * 0.4 +
                agg_scores.get("faithfulness_mean", 0) * 0.2 +
                agg_scores.get("completeness_mean", 0) * 0.1
            )
            
            leaderboard.append({
                "prompt_name": prompt_name,
                "overall_score": overall_score,
                "semantic_similarity": agg_scores.get("semantic_similarity_mean", 0),
                "accuracy": agg_scores.get("accuracy_mean", 0),
                "faithfulness": agg_scores.get("faithfulness_mean", 0),
                "completeness": agg_scores.get("completeness_mean", 0),
                "f1_score": agg_scores.get("f1_score_mean", 0),
                "exact_match": agg_scores.get("exact_match_mean", 0)
            })
        
        # Sort by overall score (descending)
        leaderboard.sort(key=lambda x: x["overall_score"], reverse=True)
        
        # Add rank
        for idx, entry in enumerate(leaderboard, 1):
            entry["rank"] = idx
        
        return leaderboard
    
    def print_leaderboard(self) -> None:
        """Print a formatted leaderboard table to console."""
        leaderboard = self.get_leaderboard_data()
        
        if not leaderboard:
            print("No evaluation results available.")
            return
        
        # Prepare table data
        table_data = []
        for entry in leaderboard:
            table_data.append([
                entry["rank"],
                entry["prompt_name"],
                f"{entry['overall_score']:.3f}",
                f"{entry['semantic_similarity']:.3f}",
                f"{entry['accuracy']:.3f}",
                f"{entry['faithfulness']:.3f}",
                f"{entry['f1_score']:.3f}"
            ])
        
        headers = [
            "Rank",
            "Prompt",
            "Overall",
            "Similarity",
            "Accuracy",
            "Faithfulness",
            "F1 Score"
        ]
        
        print("\n" + "="*80)
        print("PROMPT EVALUATION LEADERBOARD")
        print("="*80 + "\n")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
    
    def get_prompt_comparison(self, prompt1: str, prompt2: str) -> Dict[str, Any]:
        """
        Compare two prompts side-by-side.
        
        Args:
            prompt1: First prompt name
            prompt2: Second prompt name
            
        Returns:
            Comparison dictionary
        """
        leaderboard = self.get_leaderboard_data()
        
        p1_data = next((p for p in leaderboard if p["prompt_name"] == prompt1), None)
        p2_data = next((p for p in leaderboard if p["prompt_name"] == prompt2), None)
        
        if not p1_data or not p2_data:
            return {"error": "One or both prompts not found"}
        
        return {
            "prompt1": p1_data,
            "prompt2": p2_data,
            "differences": {
                metric: p1_data[metric] - p2_data[metric]
                for metric in ["overall_score", "accuracy", "faithfulness"]
            }
        }


def main():
    """Display the leaderboard when run as a script."""
    leaderboard = Leaderboard()
    leaderboard.print_leaderboard()


if __name__ == "__main__":
    main()
