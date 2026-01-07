"""
Flask web application for the Prompt Evaluation Dashboard.
"""

from flask import Flask, render_template, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from pathlib import Path
import sys
import os

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from runner import EvaluationRunner
from leaderboard import Leaderboard

# Run environment validation on startup
try:
    from validate_env import validate_environment
    validate_environment()
except ImportError:
    print("⚠️  Environment validator not found. Skipping validation.")

app = Flask(__name__)

# Configure CORS (adjust origins for production)
CORS(app, resources={
    r"/api/*": {
        "origins": os.getenv("CORS_ORIGINS", "*").split(","),
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)


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
    # Use environment variable for debug mode (never hardcode in production)
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    port = int(os.getenv('FLASK_PORT', '5000'))
    app.run(debug=debug_mode, port=port)
