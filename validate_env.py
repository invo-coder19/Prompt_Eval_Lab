"""
Environment configuration validator.
Checks for required dependencies and configuration before running the app.
"""

import sys
import os
from pathlib import Path


class EnvironmentValidator:
    """Validates environment setup and configuration."""
    
    def __init__(self):
        self.warnings = []
        self.errors = []
    
    def check_api_key(self):
        """Check if OpenAI API key is configured."""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            self.warnings.append(
                "⚠️  No OPENAI_API_KEY found. Running in DEMO MODE with heuristic evaluation.\n"
                "   To use real LLM evaluation, add your API key to .env file."
            )
        else:
            print("✅ OpenAI API key configured")
    
    def check_directories(self):
        """Ensure required directories exist."""
        required_dirs = ['results', 'prompts', 'datasets']
        for dir_name in required_dirs:
            dir_path = Path(dir_name)
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"✅ Created missing directory: {dir_name}/")
            else:
                print(f"✅ Directory exists: {dir_name}/")
    
    def check_dependencies(self):
        """Check if optional dependencies are available."""
        try:
            import openai
            print("✅ OpenAI library available")
        except ImportError:
            self.warnings.append(
                "⚠️  'openai' library not installed. Install with: pip install openai\n"
                "   Demo mode will work without it."
            )
        
        try:
            import flask
            print("✅ Flask installed")
        except ImportError:
            self.errors.append(
                "❌ Flask is required for web UI. Install with: pip install flask"
            )
        
        try:
            from sentence_transformers import SentenceTransformer
            print("✅ Sentence-transformers available")
        except ImportError:
            self.warnings.append(
                "⚠️  'sentence-transformers' not installed. Some metrics unavailable.\n"
                "   Install with: pip install sentence-transformers"
            )
    
    def check_prompts(self):
        """Verify prompt files exist."""
        prompts_dir = Path('prompts')
        prompt_files = list(prompts_dir.glob('*.txt'))
        if not prompt_files:
            self.warnings.append(
                "⚠️  No prompt files found in prompts/ directory"
            )
        else:
            print(f"✅ Found {len(prompt_files)} prompt file(s)")
    
    def check_datasets(self):
        """Verify dataset files exist."""
        datasets_dir = Path('datasets')
        dataset_files = list(datasets_dir.glob('*.json'))
        if not dataset_files:
            self.errors.append(
                "❌ No dataset files found in datasets/ directory"
            )
        else:
            print(f"✅ Found {len(dataset_files)} dataset file(s)")
    
    def validate(self):
        """Run all validation checks."""
        print("\n" + "="*70)
        print("   ENVIRONMENT VALIDATION")
        print("="*70 + "\n")
        
        self.check_directories()
        self.check_api_key()
        self.check_dependencies()
        self.check_prompts()
        self.check_datasets()
        
        # Print warnings
        if self.warnings:
            print("\n" + "="*70)
            print("   WARNINGS")
            print("="*70)
            for warning in self.warnings:
                print(f"\n{warning}")
        
        # Print errors
        if self.errors:
            print("\n" + "="*70)
            print("   ERRORS")
            print("="*70)
            for error in self.errors:
                print(f"\n{error}")
            print("\n" + "="*70)
            print("❌ Environment validation failed. Please fix the errors above.")
            print("="*70 + "\n")
            return False
        
        if not self.warnings:
            print("\n" + "="*70)
            print("✅ Environment validation passed!")
        else:
            print("\n" + "="*70)
            print("✅ Environment validation passed with warnings.")
        print("="*70 + "\n")
        return True


def validate_environment():
    """Run environment validation and return success status."""
    validator = EnvironmentValidator()
    return validator.validate()


if __name__ == '__main__':
    # Load .env if available
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    success = validate_environment()
    sys.exit(0 if success else 1)
