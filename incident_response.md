# Git Crisis Management - Incident Response Plan

## 🚨 **Emergency Scenario**
**"API keys were accidentally committed to your public repository 3 commits ago. The keys are currently active in production."**

---

## ⚡ **IMMEDIATE RESPONSE (First 15 Minutes)**

### **Phase 1: Damage Control - URGENT**

#### **Step 1: Rotate Compromised Credentials (Priority #1)**
```bash
# IMMEDIATE ACTION - Before any git cleanup
# 1. Log into your API provider dashboard
# 2. Immediately revoke/deactivate the exposed keys
# 3. Generate new API keys
# 4. Update production systems with new keys
# 5. Verify production systems are functioning with new keys
```

**⚠️ CRITICAL:** Never attempt git history cleanup before rotating credentials. Exposed keys must be considered compromised permanently.

#### **Step 2: Assess the Exposure**
```bash
# Check commit history to identify the exposure
git log --oneline -10
git show <commit-hash> | grep -i "key\|secret\|password\|token"

# Check if others have pulled the compromised commits
git log --graph --oneline --all
```

#### **Step 3: Document the Incident**
- **Time of discovery:** [Current timestamp]
- **Commits affected:** [List commit hashes]
- **Credentials exposed:** [List types - API keys, DB passwords, etc.]
- **Repository visibility:** Public
- **Estimated exposure time:** [Time since commit was pushed]

---

## 🔧 **GIT REMEDIATION (After Credential Rotation)**

### **Option A: Safe Approach (Recommended for Team Repositories)**

```bash
# 1. Create a revert commit to remove secrets
git log --oneline -5  # Find the problematic commit hash

# 2. Revert the commit that added secrets
git revert <commit-hash-with-secrets>

# 3. Add .gitignore to prevent future accidents
echo "*.key" >> .gitignore
echo "*.pem" >> .gitignore
echo ".env" >> .gitignore
echo "config.ini" >> .gitignore
echo "secrets.txt" >> .gitignore

# 4. Commit the .gitignore
git add .gitignore
git commit -m "security: add .gitignore to prevent credential commits"

# 5. Push the fix
git push origin main
```

### **Option B: History Rewrite (Only if no one else has pulled)**

```bash
# ⚠️ WARNING: Only use if you're certain no one has pulled the commits

# 1. Interactive rebase to remove the problematic commit
git rebase -i HEAD~5  # Go back 5 commits (adjust as needed)

# 2. In the editor, change 'pick' to 'drop' for the commit with secrets
# Save and exit

# 3. Force push (dangerous - use with extreme caution)
git push --force-with-lease origin main
```

### **Option C: Nuclear Option (Complete Repository Reset)**

```bash
# Only if exposure is severe and repository is personal
# 1. Create new repository
# 2. Copy clean code (without secrets)
# 3. Update all references to new repository
# 4. Delete old repository (after ensuring no data loss)
```

---

## 🛡️ **PREVENTION MEASURES IMPLEMENTATION**

### **1. Pre-commit Hooks Setup**

```bash
# Install pre-commit hooks to catch secrets
pip install pre-commit detect-secrets

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
EOF

# Install the hooks
pre-commit install

# Create initial baseline
detect-secrets scan . > .secrets.baseline
```

### **2. Environment Variable Configuration**

```bash
# Create .env.example template
cat > .env.example << EOF
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/dbname  # pragma: allowlist secret

# API Keys
API_SECRET=your-api-secret-here  # pragma: allowlist secret
THIRD_PARTY_API_KEY=your-third-party-key-here  # pragma: allowlist secret

# Security
JWT_SECRET=your-jwt-secret-here
ENCRYPTION_KEY=your-encryption-key-here
EOF

# Update application to use environment variables
# Example Python code:
```

```python
# Replace hardcoded secrets with environment variables
import os
from dotenv import load_dotenv

load_dotenv()

# Instead of:
# API_SECRET = "sk-live-1234567890abcdef"
# Use:
API_SECRET = os.environ.get('API_SECRET')
if not API_SECRET:
    raise ValueError("API_SECRET environment variable is required")
```

### **3. Enhanced .gitignore**

```bash
# Add comprehensive .gitignore
cat >> .gitignore << EOF
# Secrets and credentials
.env
.env.local
.env.production
*.key
*.pem
*.p12
*.pfx
secrets.txt
config.ini
credentials.json

# IDE and OS files
.vscode/
.idea/
.DS_Store
Thumbs.db

# Application specific
*.log
*.db
*.sqlite
temp/
cache/
EOF
```

---

## 📋 **TEAM COMMUNICATION PROTOCOL**

### **Immediate Notifications**

#### **Security Team Alert Template**
```
🚨 SECURITY INCIDENT - IMMEDIATE ACTION REQUIRED

Incident: API credentials exposed in public repository
Time: [Timestamp]
Severity: HIGH
Repository: [Repository URL]
Affected Systems: [List production systems]

IMMEDIATE ACTIONS TAKEN:
✅ Credentials rotated
✅ Production systems updated
✅ Git history being cleaned

REQUIRED ACTIONS:
- Security team: Verify no unauthorized API usage
- DevOps: Monitor production systems
- All developers: Pull latest changes after remediation

Next Update: [Time + 30 minutes]
```

#### **Team Slack/Teams Message**
```
🚨 Security Alert: API keys were accidentally committed to [repo-name]

ACTIONS REQUIRED:
1. DO NOT PULL from main branch until further notice
2. If you've already pulled recent commits, contact security team
3. All team members must update local .env files with new credentials

Status: Credentials rotated ✅
Status: Git cleanup in progress 🔄
ETA for resolution: [Time estimate]
```

### **Stakeholder Communication**

#### **Management Summary**
```
Security Incident Summary
Date: [Date]
Impact: Medium - Brief exposure of API credentials
Resolution Time: [Duration]
Business Impact: None (rapid response prevented unauthorized access)

Actions Taken:
- Immediate credential rotation
- Repository cleanup
- Prevention measures implemented
- Team training scheduled

Follow-up:
- Security audit of all repositories
- Enhanced developer training on secret management
- Implementation of automated secret scanning
```

---

## 🔍 **POST-INCIDENT ANALYSIS**

### **Root Cause Analysis**

#### **Contributing Factors**
1. **Human Error:** Developer unfamiliar with secure coding practices
2. **Process Gap:** No pre-commit hooks to catch secrets
3. **Training Gap:** Insufficient security awareness training
4. **Tool Gap:** No automated secret scanning in CI/CD

#### **Timeline of Events**
```
T-0: Developer commits code with hardcoded API key
T+5min: Code pushed to public repository
T+2hrs: Incident discovered during code review
T+2hrs 5min: Credentials rotated (immediate response)
T+2hrs 15min: Git history cleaned
T+2hrs 30min: Prevention measures implemented
T+1day: Security audit completed
```

### **Lessons Learned**

#### **What Went Well**
- ✅ Rapid incident detection (2 hours)
- ✅ Immediate credential rotation
- ✅ Effective team communication
- ✅ No evidence of credential abuse

#### **What Could Be Improved**
- ❌ Prevention: No pre-commit hooks in place
- ❌ Detection: Should have been caught earlier
- ❌ Training: Developer unaware of risks
- ❌ Process: No security checklist for commits

---

## 📚 **PREVENTION STRATEGY**

### **1. Technical Controls**

```bash
# Automated secret scanning in CI/CD
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]
jobs:
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run secret detection
        run: |
          pip install detect-secrets
          detect-secrets scan --baseline .secrets.baseline .
```

### **2. Process Controls**

#### **Developer Checklist**
- [ ] No hardcoded credentials in code
- [ ] Environment variables used for all secrets
- [ ] .env files in .gitignore
- [ ] Pre-commit hooks installed and passing
- [ ] Code review completed before merge

#### **Code Review Checklist**
- [ ] No API keys, passwords, or tokens in code
- [ ] Proper use of environment variables
- [ ] Security best practices followed
- [ ] No sensitive data in logs or comments

### **3. Training Program**

#### **Monthly Security Training Topics**
- Secure coding practices
- Git security best practices
- Environment variable management
- Incident response procedures
- Social engineering awareness

---

## 🚀 **CONTINUOUS IMPROVEMENT**

### **Monitoring and Alerting**
- GitHub secret scanning alerts enabled
- Regular repository security audits
- Automated dependency vulnerability scanning
- Log monitoring for credential usage patterns

### **Quarterly Security Reviews**
- Review all repositories for hardcoded secrets
- Update security training materials
- Test incident response procedures
- Evaluate new security tools and practices

---

**Document Owner:** Security Team
**Last Updated:** September 28, 2025
**Next Review:** December 28, 2025
**Version:** 1.0
