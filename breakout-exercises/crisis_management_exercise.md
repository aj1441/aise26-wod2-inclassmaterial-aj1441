# Git Crisis Management Exercise - Theory Breakout

**Duration:** 15 minutes  
**Format:** Group discussion (no commands run)  
**Objective:** Think through how to respond to Git disasters under time pressure

---

## 🚨 EMERGENCY SCENARIO

**ALERT:** You've just discovered that API keys were accidentally committed to your main branch **3 commits ago**. The repository is **PUBLIC** and the keys are **currently active** in your production system.

**Timeline:** This happened 2 hours ago. You need to respond immediately.

---

## Your Emergency Response (10 minutes, discussion)

### Phase 1: Immediate Damage Control (First 3 minutes)

**CRITICAL: What's your first action and why?**

Choose the correct first step:
- [ ] A) Remove the secrets from the current code
- [ ] B) Make the repository private
- [ ] C) Rotate/revoke the compromised credentials immediately
- [ ] D) Delete the problematic commits

**Why is this the right first step?**
_________________________________

### Phase 2: Git History Cleanup (Next 4 minutes)

**Situation Assessment:**
```bash
git log --oneline -5
a1b2c3d Fix user authentication bug
e4f5g6h Update README documentation  
i7j8k9l Add production configuration  ← API keys are in this commit!
m1n2o3p Add user management features
q4r5s6t Initial project setup
```

**Discuss your Git recovery approach:**

**Option A: Safe Revert (if others might have pulled)**
```bash
git revert i7j8k9l
# Creates new commit that removes the secrets
```

**Option B: History Rewrite (if you're sure no one else pulled)**
```bash
git rebase -i HEAD~3
# Remove the problematic commit entirely
```

**Which option would you choose and why?**
_________________________________

### Phase 3: Prevention Implementation (Last 3 minutes)

**Set up prevention measures:**

1. **Update .gitignore:**
```bash
# Add to .gitignore
.env
config/secrets/
*.key
credentials.json
```

2. **Create pre-commit hook (example):**
```bash
#!/bin/bash
# Check for secrets before commit
if grep -r "api_key\s*=" . ; then
    echo "❌ API key found! Use environment variables."
    exit 1
fi
```

3. **Document the incident:**
What would you write in your incident report?
_________________________________

---

## Team Discussion (5 minutes)

**Share with your breakout room:**

### Crisis Response Questions:
1. **Speed vs. Safety:** When would you choose history rewrite vs. revert?
2. **Communication:** Who would you notify during this incident?
3. **Prevention:** What other security measures could prevent this?

### Git Command Practice:
1. **Have you used `git revert` vs `git rebase -i` before?**
2. **What's the difference between `git reset` and `git revert`?**
3. **When is `git push --force` acceptable?**

### Real-World Experience:
1. **Has anyone experienced a similar incident?**
2. **What security practices does your workplace use?**
3. **How would your team handle credential rotation?**

---

---

## Common Mistakes to Avoid

❌ **Wrong:** Trying to fix Git history before rotating credentials  
✅ **Right:** Rotate credentials first, then clean history

❌ **Wrong:** Using `git push --force` without checking with team  
✅ **Right:** Use `git push --force-with-lease` or coordinate with team

❌ **Wrong:** Only removing secrets from current code  
✅ **Right:** Remove from Git history too (if possible)

❌ **Wrong:** Not implementing prevention measures  
✅ **Right:** Set up hooks and scanning to prevent recurrence

---

## Git Recovery Commands Reference

```bash
# Find lost commits
git reflog

# See what changed in a commit
git show <commit-hash>

# Undo last commit, keep changes
git reset --soft HEAD~1

# Undo last commit, lose changes  
git reset --hard HEAD~1

# Undo specific commit safely
git revert <commit-hash>

# Interactive rebase to edit history
git rebase -i HEAD~N

# Check if it's safe to force push
git push --force-with-lease
```

---

## Real-World Context

**This scenario is extremely common:**
- GitHub's secret scanning finds **millions** of exposed credentials
- **Average detection time:** 20 days for exposed secrets
- **Real impact:** AWS bills of $50,000+ from compromised keys
- **Legal implications:** GDPR fines, compliance violations

**Your response time matters:**
- **Under 1 hour:** Minimal impact if caught early
- **1-24 hours:** Moderate risk, require monitoring
- **Over 24 hours:** High risk, assume compromise

The skills you practice here directly protect production systems and prevent security incidents that can cost companies millions of dollars.