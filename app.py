"""
Flask web application for the Prompt Evaluation Dashboard.
"""

from flask import Flask, render_template, jsonify, request
from pathlib import Path
import sys

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from runner import EvaluationRunner
from leaderboard import Leaderboard

app = Flask(__name__)


@app.route('/')
def index():
    """Serve the main dashboard."""
    return render_template('index.html')


@app.route('/api/prompts')
def get_prompts():
    """Get list of available prompts."""
    prompts_dir = Path('prompts')
    prompts = [f.name for f in prompts_dir.glob('*.txt')]
    return jsonify(prompts)


@app.route('/api/evaluate', methods=['POST'])
def run_evaluation():
    """Run evaluation on selected prompts."""
    data = request.json
    selected_prompts = data.get('prompts', [])
    
    if not selected_prompts:
        return jsonify({"error": "No prompts selected"}), 400
    
    try:
        # Run evaluation
        runner = EvaluationRunner()
        runner.run_evaluation(prompt_names=selected_prompts)
        
        # Get leaderboard
        leaderboard = Leaderboard()
        leaderboard_data = leaderboard.get_leaderboard_data()
        
        return jsonify({
            "success": True,
            "leaderboard": leaderboard_data
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/leaderboard')
def get_leaderboard():
    """Get current leaderboard data."""
    try:
        leaderboard = Leaderboard()
        leaderboard_data = leaderboard.get_leaderboard_data()
        return jsonify(leaderboard_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
