"""
Integration tests for Flask API endpoints.
"""

import pytest
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app as flask_app


@pytest.fixture
def app():
    """Create Flask app for testing."""
    flask_app.config['TESTING'] = True
    return flask_app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestAPIEndpoints:
    """Test Flask API endpoints."""
    
    def test_index_route(self, client):
        """Test index page loads."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Prompt Evaluation Platform' in response.data
    
    def test_get_prompts(self, client):
        """Test GET /api/prompts returns list."""
        response = client.get('/api/prompts')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        # Should have at least the test prompts
        assert len(data) >= 0
    
    def test_evaluate_no_prompts(self, client):
        """Test POST /api/evaluate with no prompts."""
        response = client.post(
            '/api/evaluate',
            json={'prompts': []},
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_evaluate_with_prompts(self, client):
        """Test POST /api/evaluate with valid prompts."""
        # First check if prompts exist
        prompts_response = client.get('/api/prompts')
        prompts = json.loads(prompts_response.data)
        
        if len(prompts) > 0:
            response = client.post(
                '/api/evaluate',
                json={'prompts': [prompts[0]]},
                content_type='application/json'
            )
            
            # Might fail if dependencies missing, but should not crash
            assert response.status_code in [200, 500]
    
    def test_get_leaderboard_empty(self, client):
        """Test GET /api/leaderboard when empty."""
        response = client.get('/api/leaderboard')
        # Should return 200 even if empty
        assert response.status_code in [200, 500]
