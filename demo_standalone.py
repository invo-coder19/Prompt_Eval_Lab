"""
DEMO MODE - Standalone Prompt Evaluator
No API keys or external libraries required!

This demonstrates the platform using built-in Python only.
"""

import json
import re
from pathlib import Path


def simple_similarity(text1, text2):
    """Calculate basic word overlap similarity."""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0


def mock_llm_response(prompt, question, context):
    """Generate mock responses based on prompt analysis."""
    # Analyze prompt quality
    quality_score = 0
    prompt_lower = prompt.lower()
    
    if "step" in prompt_lower or "think" in prompt_lower:
        quality_score += 2
    if "accurate" in prompt_lower or "precise" in prompt_lower:
        quality_score += 1
    if len(prompt) > 150:
        quality_score += 1
    if "###" in prompt or "**" in prompt:
        quality_score += 2
    
    # Predefined answers
    answers = {
        "capital of france": "Paris",
        "romeo and juliet": "William Shakespeare",
        "chemical symbol for gold": "Au",
        "first moon landing": "1969",
        "largest planet": "Jupiter",
        "speed of light": "approximately 299,792,458 meters per second",
        "mona lisa": "Leonardo da Vinci"
    }
    
    # Find answer
    q_lower = question.lower()
    answer = None
    for key, value in answers.items():
        if key in q_lower:
            answer = value
            break
    
    if not answer:
        answer = "Demo answer"
    
    # Vary detail based on prompt quality
    if quality_score >= 4:
        return f"Based on the provided context, {answer}. This answer is derived from the given information."
    elif quality_score >= 2:
        return answer
    else:
        return answer.split()[0] if answer.split() else answer


def evaluate_output(output, reference):
    """Simple heuristic evaluation."""
    similarity = simple_similarity(output, reference)
    
    # Length comparison
    len_ratio = min(len(output), len(reference)) / max(len(output), len(reference), 1)
    
    # Token overlap F1
    out_words = set(output.lower().split())
    ref_words = set(reference.lower().split())
    
    if ref_words:
        overlap = len(ref_words.intersection(out_words)) / len(ref_words)
    else:
        overlap = 0.0
    
    accuracy = (similarity + overlap + len_ratio * 0.5) / 2.5
    faithfulness = accuracy * 0.95 if len(output) < len(reference) * 3 else accuracy * 0.8
    completeness = overlap
    
    return {
        "semantic_similarity": min(1.0, similarity + 0.3),
        "accuracy": min(1.0, max(0.3, accuracy)),
        "faithfulness": min(1.0, max(0.3, faithfulness)),
        "completeness": min(1.0, max(0.3, completeness)),
        "f1_score": overlap,
        "exact_match": 1.0 if output.lower().strip() == reference.lower().strip() else 0.0
    }


def run_demo():
    """Run the demo evaluation."""
    print("\n" + "="*70)
    print("   [DEMO] PROMPT EVALUATION PLATFORM - STANDALONE MODE")
    print("="*70)
    print("   No API keys or external libraries required!")
    print("   Using built-in heuristic evaluation\n")
    
    # Load dataset
    dataset_path = Path("datasets") / "qa_test.json"
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    # Load prompts
    prompts_dir = Path("prompts")
    prompt_files = sorted(prompts_dir.glob("*.txt"))
    
    all_results = []
    
    for prompt_file in prompt_files:
        print(f"\n{'='*70}")
        print(f"Evaluating: {prompt_file.name}")
        print(f"{'='*70}\n")
        
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
        
        scores_list = []
        
        for idx, test_case in enumerate(dataset[:5], 1):  # First 5 for demo
            question = test_case["question"]
            reference = test_case["reference_answer"]
            context = test_case.get("context", "")
            
            # Generate response
            full_prompt = prompt_template.replace("{question}", question).replace("{context}", context)
            output = mock_llm_response(prompt_template, question, context)
            
            # Evaluate
            scores = evaluate_output(output, reference)
            scores_list.append(scores)
            
            print(f"Test {idx}: {question[:50]}...")
            print(f"  Output: {output[:60]}...")
            print(f"  Similarity: {scores['semantic_similarity']:.3f} | Accuracy: {scores['accuracy']:.3f}")
        
        # Calculate averages
        avg_scores = {}
        for key in scores_list[0].keys():
            avg_scores[f"{key}_mean"] = sum(s[key] for s in scores_list) / len(scores_list)
        
        # Calculate overall score
        overall = (
            avg_scores.get("semantic_similarity_mean", 0) * 0.3 +
            avg_scores.get("accuracy_mean", 0) * 0.4 +
            avg_scores.get("faithfulness_mean", 0) * 0.2 +
            avg_scores.get("completeness_mean", 0) * 0.1
        )
        
        all_results.append({
            "prompt_name": prompt_file.name,
            "overall_score": overall,
            "scores": avg_scores
        })
    
    # Print leaderboard
    print(f"\n\n{'='*70}")
    print("   [LEADERBOARD] Final Rankings")
    print(f"{'='*70}\n")
    
    all_results.sort(key=lambda x: x["overall_score"], reverse=True)
    
    print(f"{'Rank':<6} {'Prompt':<20} {'Overall':<10} {'Similarity':<12} {'Accuracy':<10}")
    print("-" * 70)
    
    for rank, result in enumerate(all_results, 1):
        medal = "[1]" if rank == 1 else "[2]" if rank == 2 else "[3]" if rank == 3 else f" {rank}."
        print(f"{medal:<6} {result['prompt_name']:<20} "
              f"{result['overall_score']:.3f}      "
              f"{result['scores']['semantic_similarity_mean']:.3f}        "
              f"{result['scores']['accuracy_mean']:.3f}")
    
    print("\n" + "="*70)
    print("   [SUCCESS] Demo complete!")
    print("   Notice: Better prompts (v2, v3) score higher than basic v1")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_demo()
