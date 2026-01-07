# Contributing to Prompt Evaluation Lab

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Prompt_Eval_Lab.git`
3. Create a branch: `git checkout -b feature/your-feature-name`

## Development Setup

```bash
# Install dependencies
pip install -r requirements-dev.txt

# Run environment validation
python validate_env.py

# Run tests
pytest tests/

# Run linting
flake8 src/ app.py
black --check src/ app.py
```

## Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting (`black src/ app.py`)
- Maximum line length: 100 characters
- Add docstrings to all functions and classes
- Type hints are encouraged

## Testing

- Write tests for new features
- Maintain test coverage above 80%
- Run full test suite before submitting PR

```bash
pytest tests/ -v --cov=src
```

## Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit PR with clear description

## Commit Messages

Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `style:` Formatting changes

Example: `feat: add export to PDF functionality`

## Questions?

Open an issue for discussion before starting major changes.
