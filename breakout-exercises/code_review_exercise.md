# Code Review Exercise - In-Class Breakout

**Duration:** 15 minutes  
**Format:** Individual work with team discussion  
**Objective:** Practice identifying security vulnerabilities and writing professional code review comments

---

## The Code to Review

You're reviewing this Python authentication code that has multiple security issues. Your job is to find them and provide professional feedback.

```python
# auth_system.py - Find the security issues
import requests
import sqlite3
import hashlib

API_KEY = "sk-live-1234567890abcdef"
DATABASE_URL = "postgresql://admin:password123@localhost/prod"
DEBUG_MODE = True

def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    
    result = conn.execute(query).fetchone()
    
    print(f"Login attempt: {username}:{password}")
    
    response = requests.post("https://api.auth.com/verify", 
                           data={"user": username, "key": API_KEY})
    
    return response.json()

def reset_password(user_id, new_password):
    conn = sqlite3.connect("users.db")
    query = f"UPDATE users SET password='{new_password}' WHERE id={user_id}"
    conn.execute(query)
    conn.commit()
    
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def admin_check(user_id):
    if user_id == 1 or user_id == "admin":
        return True
    return False
```

---

## Your Task (10 minutes individual work)

**Find and document at least 6 security issues** using this professional format:

```markdown
## Code Review Comments

**🔴 SECURITY: [Issue Type]**
**Line X:** [Specific problem description]
**Impact:** [What could go wrong if exploited]
**Suggestion:** 
```python
# Instead of this vulnerable code:
vulnerable_example()

# Use this secure approach:
secure_example()
```
**Priority:** Critical/High/Medium/Low
```

---

## Hints

- Look for hardcoded secrets and credentials
- Check for SQL injection risks in string-formatted queries
- Watch for logging of sensitive data
- Ensure passwords are hashed with modern algorithms
- Validate inputs and handle errors
- Avoid insecure external API usage without checking responses
- Beware of hidden backdoors and insecure defaults

---

## Team Discussion (5 minutes)

**Share with your breakout room:**
1. Which issues did you find?
2. Which ones did you miss?
3. How would you prioritize fixing them?
4. What was challenging about writing professional review comments?

**Discussion Questions:**
- What makes a code review comment helpful vs. just critical?
- How do you balance being thorough with being constructive?
- What would you want to see in a review of your own code?

---

---

## Real-World Application

These are the exact types of issues you'll encounter in professional code reviews:
- **Hardcoded secrets** appear in ~15% of repositories
- **SQL injection** remains a top security vulnerability
- **Weak password hashing** affects millions of users
- **Missing input validation** leads to data breaches

The review skills you practice here directly apply to protecting your team's production systems.