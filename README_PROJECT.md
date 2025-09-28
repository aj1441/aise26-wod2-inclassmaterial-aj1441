# Secure Flask API - Professional Repository

A professionally configured Flask API with security best practices, automated testing, and CI/CD pipeline.

## 🚀 Features

- **User Authentication System**: Secure user registration and login
- **CRUD Operations**: RESTful API endpoints for user management
- **Security First**: Multiple security layers and vulnerability scanning
- **Automated Testing**: Comprehensive test suite with coverage reporting
- **CI/CD Pipeline**: Automated quality gates and deployment

## 🔒 Security Measures

### Implemented Security Features
- ✅ Secure password hashing (bcrypt)
- ✅ SQL injection prevention (parameterized queries)
- ✅ Input validation and sanitization
- ✅ Secure logging (no sensitive data exposure)
- ✅ Environment-based configuration
- ✅ Pre-commit hooks for secret detection
- ✅ Automated security scanning with Bandit

### Security Scanning
This repository uses multiple security tools:
- **Bandit**: Python security linter
- **Safety**: Dependency vulnerability checking
- **detect-secrets**: Pre-commit hook for secret detection
- **GitHub Actions**: Automated security scanning in CI/CD

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment support

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   ```

2. **Set up Python virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Run the application**
   ```bash
   cd starter-code-simple
   python app.py
   ```

7. **Access the API**
   - Health check: `http://localhost:5000/health`
   - Users endpoint: `http://localhost:5000/users`

## 📊 API Endpoints

### Health Check
```
GET /health
```
Returns the application health status.

### User Management
```
GET /users          # List all users
POST /users         # Create a new user
POST /login         # User authentication
```

### Example Usage
```bash
# Create a user
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "securepassword123"}'

# Login
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "securepassword123"}'
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run security tests
bandit -r .
```

### Test Coverage
Current test coverage: [Coverage Badge]

## 🔄 Development Workflow

### Branch Protection Rules
- **Main branch** is protected
- Requires pull request reviews (minimum 1)
- Status checks must pass before merging
- Administrators included in restrictions

### Pull Request Process
1. Create feature branch from `main`
2. Make changes following coding standards
3. Run tests and security checks locally
4. Create pull request using the template
5. Address review feedback
6. Merge after approval and passing CI/CD

### Code Quality Standards
- **Formatting**: Black formatter
- **Import sorting**: isort
- **Linting**: Flake8
- **Security**: Bandit scanning
- **Testing**: Minimum 80% coverage

## 📋 Contributing Guidelines

### Before Contributing
1. Read our [Code of Conduct](CODE_OF_CONDUCT.md)
2. Check existing issues and pull requests
3. Follow our coding standards and security practices

### Development Process
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run tests and security checks
5. Commit with descriptive messages
6. Push to your fork
7. Create a pull request

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `security`

## 🚨 Security

### Reporting Security Vulnerabilities
If you discover a security vulnerability, please:
1. **Do not** create a public GitHub issue
2. Send details to [security@yourorg.com]
3. Include steps to reproduce
4. Allow time for assessment and fix

### Security Best Practices
- Never commit secrets or credentials
- Use environment variables for configuration
- Keep dependencies updated
- Follow OWASP security guidelines
- Run security scans before deployment

## 📈 CI/CD Pipeline

### Automated Checks
- ✅ Security scanning (Bandit, Safety)
- ✅ Code quality (Black, isort, Flake8)
- ✅ Testing (pytest with coverage)
- ✅ Dependency vulnerability scanning

### Deployment
- Automatic deployment to staging on `develop` branch
- Manual deployment to production from `main` branch
- Zero-downtime deployments with health checks

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgments

- Flask framework team
- Security tools maintainers
- Contributors and reviewers

## 📞 Support

- Documentation: [Wiki](../../wiki)
- Issues: [GitHub Issues](../../issues)
- Discussions: [GitHub Discussions](../../discussions)

---

**Note**: This is a educational project demonstrating professional Git workflows and security practices.
