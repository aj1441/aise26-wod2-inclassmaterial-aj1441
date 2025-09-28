# Contributing Guidelines

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributors.

## 🎯 Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:
- Be respectful and inclusive
- Use welcoming and inclusive language
- Be collaborative and constructive
- Focus on what's best for the community
- Show empathy towards other community members

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git
- Familiarity with Flask and web APIs
- Understanding of security best practices

### Development Setup
1. Fork the repository
2. Clone your fork locally
3. Set up the development environment (see README.md)
4. Install pre-commit hooks: `pre-commit install`

## 🔄 Workflow

### Branch Strategy
- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: Individual feature branches
- `hotfix/*`: Critical fixes for production
- `security/*`: Security-related fixes (high priority)

### Making Changes

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow coding standards (see below)
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run all tests
   pytest

   # Run security checks
   bandit -r .
   pre-commit run --all-files

   # Check code quality
   black --check .
   isort --check-only .
   flake8 .
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat(auth): add secure password hashing"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 Coding Standards

### Python Style
- **Formatter**: Black (line length: 88 characters)
- **Import sorting**: isort with Black profile
- **Linting**: Flake8 with security focus
- **Docstrings**: Google style docstrings

### Security Requirements
- ✅ No hardcoded secrets or credentials
- ✅ Input validation for all user inputs
- ✅ Parameterized SQL queries (no string concatenation)
- ✅ Secure logging (no sensitive data in logs)
- ✅ Error handling that doesn't expose internal details
- ✅ Security headers in HTTP responses

### Code Example
```python
def create_user(username: str, password: str) -> dict:
    """Create a new user with secure password hashing.

    Args:
        username: The username (validated)
        password: The plain text password

    Returns:
        dict: User creation result

    Raises:
        ValueError: If validation fails
        DatabaseError: If database operation fails
    """
    # Validate inputs
    if not username or len(username) < 3:
        raise ValueError("Username must be at least 3 characters")

    if not is_strong_password(password):
        raise ValueError("Password does not meet security requirements")

    # Secure password hashing
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        # Use parameterized queries
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        return {"success": True, "username": username}
    except DatabaseError as e:
        logger.error(f"Database error during user creation: {e}")
        raise DatabaseError("Failed to create user")
```

## 🧪 Testing Guidelines

### Test Requirements
- **Unit tests**: For all new functions and classes
- **Integration tests**: For API endpoints
- **Security tests**: For security-critical functionality
- **Coverage**: Minimum 80% code coverage

### Test Structure
```python
def test_create_user_success():
    """Test successful user creation."""
    # Arrange
    username = "testuser"
    password = "SecurePass123!"

    # Act
    result = create_user(username, password)

    # Assert
    assert result["success"] is True
    assert result["username"] == username

def test_create_user_sql_injection_protection():
    """Test SQL injection protection."""
    malicious_username = "'; DROP TABLE users; --"
    password = "password123"

    with pytest.raises(ValueError):
        create_user(malicious_username, password)
```

## 📋 Pull Request Guidelines

### PR Checklist
- [ ] Branch is up to date with target branch
- [ ] All tests pass locally
- [ ] Security checks pass
- [ ] Code follows style guidelines
- [ ] Documentation updated (if needed)
- [ ] PR template completed

### PR Title Format
```
type(scope): brief description

Examples:
feat(auth): add multi-factor authentication
fix(api): resolve SQL injection vulnerability
docs(readme): update installation instructions
security(auth): implement rate limiting
```

### PR Description
Use our PR template and include:
- **What**: What changes were made
- **Why**: Why the changes were necessary
- **How**: How the changes were implemented
- **Testing**: What testing was performed
- **Security**: Any security implications

## 🔒 Security Contributions

### Security-First Approach
All contributions must prioritize security:
1. **Threat modeling**: Consider potential security impacts
2. **Input validation**: Validate all user inputs
3. **Output encoding**: Properly encode outputs
4. **Authentication**: Verify user identity
5. **Authorization**: Check user permissions
6. **Encryption**: Use strong encryption for sensitive data

### Security Review Process
Security-related changes require:
1. Security impact assessment
2. Additional reviewer with security expertise
3. Penetration testing (if applicable)
4. Documentation of security measures

## 🐛 Bug Reports

### Before Reporting
- Check existing issues
- Verify it's not a known issue
- Test with the latest version

### Bug Report Template
```markdown
**Bug Description**
A clear description of the bug.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected Behavior**
What you expected to happen.

**Security Impact**
Any potential security implications.

**Environment**
- OS: [e.g. macOS, Linux, Windows]
- Python version: [e.g. 3.9.0]
- Flask version: [e.g. 2.3.2]

**Additional Context**
Any other context about the problem.
```

## 🆘 Getting Help

### Resources
- **Documentation**: Check the project wiki
- **Discussions**: Use GitHub Discussions for questions
- **Issues**: Report bugs and feature requests
- **Security**: Email security@yourorg.com for security issues

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Email**: security@yourorg.com for security concerns

## 🏆 Recognition

Contributors will be recognized in:
- **Contributors section**: In README.md
- **Release notes**: For significant contributions
- **Hall of Fame**: For exceptional contributions

## 📚 Additional Resources

### Learning Resources
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Guide](https://python-security.readthedocs.io/)
- [Flask Security](https://flask-security-too.readthedocs.io/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)

### Tools Documentation
- [Black](https://black.readthedocs.io/)
- [Bandit](https://bandit.readthedocs.io/)
- [pytest](https://docs.pytest.org/)
- [Pre-commit](https://pre-commit.com/)

---

Thank you for contributing! Your efforts help make this project more secure and robust for everyone. 🙏
