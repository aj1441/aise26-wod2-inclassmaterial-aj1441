## 🔒 Security Checklist

Before merging this PR, please ensure all security requirements are met:

### 📋 Code Review
- [ ] Code has been reviewed by at least one team member
- [ ] No hardcoded secrets, passwords, or API keys
- [ ] Input validation is implemented for user inputs
- [ ] SQL queries use parameterized statements (no string concatenation)
- [ ] Sensitive data is not logged or exposed in error messages
- [ ] Authentication and authorization checks are in place

### 🛡️ Security Scanning
- [ ] Pre-commit hooks passed (no secrets detected)
- [ ] Bandit security scanner passed
- [ ] No high or critical security vulnerabilities introduced
- [ ] Dependencies are up to date and secure

### 🧪 Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Security tests pass
- [ ] Manual testing completed

### 📚 Documentation
- [ ] Code is properly documented
- [ ] README updated if needed
- [ ] Security implications documented
- [ ] Breaking changes documented

## 📝 Description

Brief description of changes:

## 🔄 Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Security fix
- [ ] Documentation update

## 🧪 How Has This Been Tested?

Describe the tests that you ran to verify your changes:

## 📷 Screenshots (if applicable)

## 📋 Additional Notes

Any additional information, context, or notes for reviewers:

---

### 🚨 Security Notice
This PR has been reviewed for security vulnerabilities. By merging this PR, you acknowledge that:
- All security checks have been completed
- No known security vulnerabilities are being introduced
- Proper security practices have been followed
