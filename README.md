# Professional Git Workflows — Student Guide

## Overview
**Format:** In-class breakout exercises + after-class individual assignment  
**Language:** Python  
**Skills:** Professional Git workflows, code reviews, merge conflicts, security

---

## Learning Objectives
By completing this assignment, you will:
- Design custom Git workflows that fit team needs
- Write professional pull requests and provide constructive code reviews  
- Resolve merge conflicts systematically and safely
- Implement security best practices and catch common vulnerabilities
- Set up automated quality gates with branch protection and hooks
- Handle Git disasters and recovery scenarios

---

## How This Works

### In Class
- Complete the breakout exercises in `breakout-exercises/` locally with classmates:
  - Code Review
  - Merge Conflict Resolution
  - Crisis Management

### After Class (Your Assignment)
- Take the provided starter code in `starter-code-simple/` and create your own repository from it.
- You can either:
  1) Fork/clone this repository and push to a new repo you own, or  
  2) If you received a GitHub Classroom link, accept it to create your student repo, then copy the starter code into that repo and complete all steps there.
- Then complete all professionalization steps below using your own repository.

Note: Some repository settings (like branch protection) require repository admin permissions. On a GitHub Classroom repo you typically have admin access; if not, create your own repository so you can configure everything.

### Part 1: Repository Setup & Security

#### Your Task
Transform the provided basic Python API into a professionally configured repository with security measures.

#### Starter Code
You'll receive a basic Flask API with intentional security issues:
- User authentication system
- Basic CRUD operations  
- Configuration management
- Simple database integration

#### Requirements
1. **Branch Protection Setup**
   - Configure branch protection rules for main branch
   - Require pull request reviews (minimum 1)
   - Require status checks to pass before merging
   - Include administrators in restrictions

2. **Security Implementation**
   - Set up pre-commit hooks to catch hardcoded secrets
   - Configure automated security scanning (bandit for Python)
   - Create custom security checks for your codebase
   - Add proper .gitignore for Python projects

3. **Professional Documentation**
   - Create comprehensive README with setup instructions
   - Add pull request template with security checklist
   - Document your team workflow and standards
   - Include contributing guidelines

4. **CI/CD Pipeline**
   - Set up GitHub Actions for automated testing
   - Add code quality checks (linting, formatting)
   - Include security scanning in pipeline

---

### Part 2: Code Review Mastery (In Class)

#### Your Task
Review the provided Python authentication code and identify security vulnerabilities, then provide professional feedback.

#### Code Review Exercise
You'll review code with multiple security issues including:
- Hardcoded secrets and credentials
- SQL injection vulnerabilities
- Weak password hashing
- Missing input validation
- Insecure logging practices

#### What to Produce
1. **Vulnerability Identification**
   - Identify at least 8 distinct security issues
   - Categorize issues by severity (Critical, High, Medium, Low)
   - Provide specific line numbers and explanations

2. **Professional Review Comments**
   - Write 5 constructive review comments
   - Use professional, helpful language
   - Provide specific code examples for fixes
   - Include security impact assessments

**Template for Review Comments:**
```markdown
**🔴 SECURITY: [Issue Type]**
**Line X:** [Specific problem description]
**Impact:** [What could go wrong]
**Suggestion:** 
```python
# Instead of this vulnerable code:
old_code_example()

# Use this secure approach:
secure_code_example()
```
**Priority:** Critical/High/Medium/Low
```

---

### Part 3: Merge Conflict Resolution (In Class)

#### Scenario
You'll work through a realistic merge conflict where two developers added different features to the same Python API:
- **Branch A:** Added authentication and input validation
- **Branch B:** Added database integration and user management

#### Your Task
Resolve the conflict by intelligently combining both features rather than simply choosing one side.

#### What to Produce
1. **Intelligent Resolution**
   - Combine functionality from both branches
   - Maintain all important features
   - Ensure code follows Python best practices
   - Test that merged code works correctly

2. **Documentation**
   - Document your resolution decisions
   - Explain why you chose specific approaches
   - Create clear commit message explaining the resolution

---

### Part 4: Git Crisis Management (In Class)

#### Emergency Scenario
"API keys were accidentally committed to your public repository 3 commits ago. The keys are currently active in production."

#### Your Response
1. **Immediate Actions**
   - Identify the correct first steps (credential rotation)
   - Choose appropriate Git commands for cleanup
   - Implement prevention measures

2. **Documentation**
   - Create incident response documentation
   - Document prevention measures implemented
   - Create team procedures for future incidents

#### Git Recovery Commands You'll Use
```bash
# Find the problematic commit
git log --oneline -10

# Remove secrets from history (if safe)
git rebase -i HEAD~5

# Or revert if others have pulled
git revert <commit-hash>

# Implement prevention
# Set up pre-commit hooks
# Add secrets to .gitignore
```

---

## Breakouts (In Class)
Use the files in `breakout-exercises/` during class. Discuss approaches with your group, but submit your own work in your personal repository.

---

## What to Submit (After Class)

### GitHub Repository
Your final repository must include:
- [ ] Working branch protection rules
- [ ] Security scanning and pre-commit hooks configured
- [ ] Professional documentation (README, PR template, contributing guidelines)
- [ ] CI/CD pipeline running successfully
- [ ] All security vulnerabilities from starter code fixed

### Written Components
Submit via your repository:
1. **Code Review Report** (`code_review.md`)
   - List of security vulnerabilities found
   - Professional review comments
   - Explanation of severity ratings

2. **Merge Resolution Report** (`merge_resolution.md`)
   - Description of conflict scenario
   - Explanation of resolution approach
   - Documentation of testing performed

3. **Incident Response Plan** (`incident_response.md`)
   - Step-by-step crisis response procedures
   - Prevention measures implemented
   - Team communication protocols

---

## Evaluation Guide

### Technical Implementation
- **Repository Setup:** Branch protection, security measures, documentation
- **Security Fixes:** Resolution of vulnerabilities in starter code
- **CI/CD Implementation:** Working automated pipeline

### Professional Skills
- **Code Review Quality:** Professional, actionable feedback
- **Conflict Resolution:** Intelligent merging that preserves functionality

### Documentation & Process
- **Written Communication:** Clear, professional documentation
- **Process Documentation:** Usable procedures for team workflows

---

---

## Resources

### Git Documentation
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Interactive Git Tutorial](https://learngitbranching.js.org/)

### Security Resources
- [OWASP Python Security](https://owasp.org/www-project-python-security/)
- [Bandit Security Scanner](https://bandit.readthedocs.io/)
- [Python Security Best Practices](https://python-security.readthedocs.io/)

### GitHub Features
- [Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Code Review Best Practices](https://github.com/features/code-review/)

---

## Getting Started
1. Create a new repository you own (or accept your GitHub Classroom repo if provided). Ensure you have admin access so you can configure branch protection and settings.
2. Copy the contents of `starter-code-simple/` into your repository.
3. Install and run the app:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
4. Create a working branch. Implement changes via pull requests with reviews (ask a peer to review).
5. Add security scanning, pre-commit hooks, CI, and docs. Configure branch protection on `main`.
6. Complete the three breakout exercises as practice; then finalize your repository and written components.