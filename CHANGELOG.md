# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2026-01-07

### Added
- **Testing Infrastructure**: Complete pytest suite with 30+ tests covering evaluator, metrics, runner, and API
- **Docker Support**: Dockerfile, docker-compose.yml, and development compose for easy deployment
- **Security Features**: API rate limiting (50/hour, 200/day), CORS configuration, input validation
- **Performance**: Lazy loading for SentenceTransformer model (~2-3s faster startup)
- **Enhanced Dataset**: Expanded from 7 to 15 questions across multiple categories
- **Environment Validation**: Automatic validation on startup with helpful warnings
- **Toast Notifications**: Elegant UI notifications replacing browser alerts
- **CI/CD**: GitHub Actions workflow for automated testing and linting
- **Documentation**: DEPLOYMENT.md, CONTRIBUTING.md, and improved inline documentation

### Changed
- **Dependencies**: Updated to latest versions with proper version constraints (openai >=1.50.0, etc.)
- **Debug Mode**: Now controlled by environment variable (FLASK_DEBUG) instead of hardcoded
- **Requirements**: Split into requirements.txt (prod) and requirements-dev.txt (dev/test)

### Fixed
- Typo in README.md: "perfom" → "perform"
- Typo in README.md: Missing space in "##Project Structure"
- Typo in demo_standalone.py: Missing space in "#Token overlap F1"

### Security
- Removed hardcoded debug=True in production
- Added rate limiting to prevent API abuse
- Implemented CORS with configurable origins
- Added environment-based configuration

## [1.0.0] - 2026-01-06

### Added
- Initial release
- Standalone demo mode with no API requirements
- Full LLM evaluation mode with OpenAI API
- Web dashboard with modern UI
- Three sample prompts (v1, v2, v3)
- Metrics: semantic similarity, accuracy, faithfulness, completeness
- 7-question test dataset
