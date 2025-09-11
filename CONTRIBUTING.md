# Contributing to Discernus

Thank you for your interest in contributing to Discernus! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and constructive in all interactions.

## Getting Started

### Prerequisites
- Python 3.13+
- Git
- Basic understanding of the project architecture

### Development Setup
1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/discernus.git`
3. Install in development mode: `pip install -e .`
4. Install development dependencies: `pip install -e .[dev]`
5. Run tests: `make test`

## Types of Contributions

### Bug Reports
- Use the bug report template
- Provide clear reproduction steps
- Include error logs and environment details
- Search existing issues first

### Feature Requests
- Use the feature request template
- Explain the use case and value
- Consider implementation complexity
- Discuss with maintainers first for large features

### Code Contributions
- Fork the repository
- Create a feature branch
- Make your changes
- Add tests for new functionality
- Ensure all tests pass
- Submit a pull request

### Documentation
- Improve existing documentation
- Add examples and tutorials
- Fix typos and clarify explanations
- Update API documentation

### Framework Contributions
- Submit new framework specifications
- Improve existing frameworks
- Add framework validation tools
- Create framework examples

## Development Workflow

### Branching Strategy
- `main` - Stable releases
- `develop` - Development branch
- `feature/*` - Feature branches
- `hotfix/*` - Critical fixes

### Pull Request Process
1. Create a feature branch from `develop`
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Update documentation if needed
6. Submit pull request to `develop`

### Code Style
- Follow PEP 8
- Use `black` for formatting
- Use `isort` for import sorting
- Use `flake8` for linting
- Maximum line length: 120 characters

### Testing
- Write unit tests for new functionality
- Ensure existing tests pass
- Aim for high test coverage
- Test edge cases and error conditions

### Documentation
- Update docstrings for new functions
- Add examples where helpful
- Update README if needed
- Keep documentation current

## Framework Development

### Framework Structure
Frameworks should follow the specification format:
- Clear description and purpose
- Academic references
- Measurable dimensions
- Validation criteria

### Framework Validation
- Test with sample data
- Ensure reproducibility
- Validate against specifications
- Document limitations

### Framework Submission
1. Create framework specification
2. Add validation tests
3. Include example usage
4. Submit pull request
5. Address review feedback

## Issue Labels

### Bug Labels
- `bug` - General bug
- `critical` - Critical bug
- `regression` - Regression bug
- `needs-triage` - Needs initial review

### Feature Labels
- `enhancement` - New feature
- `framework` - Framework-related
- `cli` - CLI-related
- `documentation` - Documentation

### Priority Labels
- `high` - High priority
- `medium` - Medium priority
- `low` - Low priority

### Status Labels
- `needs-triage` - Needs initial review
- `in-progress` - Currently being worked on
- `needs-review` - Ready for review
- `blocked` - Blocked on something

## Release Process

### Version Numbering
We use semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version number bumped
- [ ] Release notes prepared

## Community Guidelines

### Communication
- Be respectful and constructive
- Use clear and concise language
- Provide context for questions
- Help others when possible

### Reporting Issues
- Search existing issues first
- Use appropriate templates
- Provide sufficient detail
- Be patient with responses

### Contributing Code
- Follow coding standards
- Write clear commit messages
- Test your changes
- Respond to feedback

## Getting Help

### Documentation
- Check the documentation first
- Look for existing issues
- Search the codebase

### Community Support
- GitHub Discussions for questions
- GitHub Issues for bugs
- Discord/Slack for real-time chat

### Maintainer Contact
- @discernus-team for general questions
- @discernus-maintainers for technical issues

## License

By contributing to Discernus, you agree that your contributions will be licensed under the same license as the project (GPL v3.0-or-later).

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation
- Community acknowledgments

Thank you for contributing to Discernus!
