# Contributing to Trackify

Thank you for your interest in contributing to Trackify! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version, etc.)
- Any relevant logs or error messages

### Suggesting Features

Feature suggestions are welcome! Please create an issue with:
- A clear description of the feature
- The problem it solves
- Any implementation ideas you have

### Pull Requests

1. **Fork the repository** and create a new branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards:
   - Write clear, descriptive commit messages
   - Add tests for new functionality
   - Update documentation as needed
   - Follow PEP 8 style guidelines
   - Add type hints to all functions

3. **Test your changes**
   ```bash
   # Run tests
   pytest

   # Run type checking
   mypy src/

   # Run code formatting
   black src/ tests/

   # Run security checks
   bandit -r src/
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

   Use conventional commit messages:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for test additions/changes
   - `refactor:` for code refactoring
   - `chore:` for maintenance tasks

5. **Push to your fork** and create a pull request
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** with:
   - A clear title and description
   - Reference to any related issues
   - Screenshots (if applicable)
   - Test results

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/trackify.git
   cd trackify
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

5. Create a `.env` file with your test credentials:
   ```bash
   cp .env.example .env
   # Edit .env with your test API keys
   ```

## Coding Standards

### Python Style
- Follow PEP 8
- Use Black for code formatting (line length: 88)
- Use meaningful variable and function names
- Add docstrings to all public functions and classes

### Type Hints
- Add type hints to all function signatures
- Use `typing` module for complex types
- Run MyPy to verify type correctness

### Testing
- Write unit tests for all new functionality
- Aim for >80% code coverage
- Use pytest fixtures for common setup
- Use VCR for recording API interactions
- Mock external dependencies

### Documentation
- Update README.md for user-facing changes
- Add docstrings following Google style
- Update CHANGELOG.md following Keep a Changelog format
- Include code examples in docstrings

## Project Structure

```
trackify/
├── src/
│   ├── clients/          # API client implementations
│   ├── generators/       # Report generators
│   ├── orchestrator/     # Main workflow coordinator
│   ├── shared/          # Shared DTOs and utilities
│   └── utils/           # Utility functions
├── tests/               # Test files
├── docs/                # Documentation
└── main.py             # CLI entry point
```

## Questions?

If you have questions, feel free to:
- Open an issue for discussion
- Reach out to the maintainers
- Check existing issues and pull requests

Thank you for contributing to Trackify! 🚀
