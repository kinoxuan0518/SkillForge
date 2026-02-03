# SkillForge Best Practices

Guide for creating high-quality, maintainable skills.

## 1. Writing Effective Trigger Phrases

### Good Triggers Are:
- **Specific**: "create a Python linting skill" not "make a skill"
- **Action-oriented**: "turn X into a skill", "make a skill for X"
- **Natural**: Phrases users would actually say
- **Diverse**: Cover different ways to express the same need

### Examples

✅ **Good**
```
- "make a skill for Python linting"
- "create a linting skill"
- "turn my linting setup into a reusable method"
- "沉淀 Python 代码检查成 Skill"
- "turn linting into skill"
```

❌ **Bad**
```
- "skill" (too generic)
- "python" (too broad)
- "make something" (too vague)
```

---

## 2. Defining Scope Properly

### The "Rule of 3"
- **3+ must-cover items**: Ensures sufficient scope
- **3+ must-not-cover items**: Prevents scope creep
- **5+ trigger phrases**: Multiple entry points

### Red Flags
- Single goal with 10+ must-cover items → Split into sub-skills
- Must-cover and must-not-cover overlap → Redefine boundary
- Trigger phrases all identical → Add more variations

---

## 3. Writing Excellent Failure Modes

### Structure: Symptom → Root Cause → Fix

```markdown
**Symptom**: Expected behavior not observed
**Root Cause**: [Why it happens]
**Fix**: [Step-by-step solution]
```

### Brainstorm Failures
Ask for each aspect:
- What if input is empty?
- What if input is malformed?
- What if the tool/service is unavailable?
- What if user has wrong permissions?
- What if format/version is unexpected?
- What if network is slow/unreliable?
- What if edge case is hit?

### Real-World Examples

**Python Package Import**
```
Symptom: "ModuleNotFoundError: No module named 'X'"
Root Cause: Package not installed in environment
Fix: Run 'pip install X' then retry
```

**API Rate Limit**
```
Symptom: "429 Too Many Requests" error
Root Cause: Exceeded API rate limits
Fix: Wait 1 hour before retry, or upgrade API plan
```

**Encoding Issue**
```
Symptom: Garbled characters in output (🚨️️ or ????)
Root Cause: Character encoding mismatch
Fix: Ensure input file is UTF-8 encoded
```

---

## 4. Identifying Edge Cases

Ask about:

**Input variations**
- Empty input
- Very large input
- Special characters (emoji, accents, symbols)
- Whitespace variations
- Type mismatches

**Environment variations**
- Different operating systems (Windows/Mac/Linux)
- Different shell environments (bash/zsh/fish)
- Missing optional dependencies
- Path/permission issues

**Behavioral variations**
- Partial success (some items succeed, some fail)
- Idempotency (running twice gives same result?)
- Concurrency (what if run in parallel?)
- State dependencies (does order matter?)

---

## 5. Creating Reusable Templates

### Good Templates Are:
- **Practical**: Can be copy-pasted and used immediately
- **Minimal**: Include only essential parts
- **Documented**: Brief comments explaining each section
- **Variations**: Show 2-3 different use cases

### Template Structure
```
## [Template Name]

[Brief description of when to use]

```[language]
[Commented code/config]
```

**When to use**: [Conditions]
**Common variations**: [Alternatives]
```

### Real Template Example

## Python Logging Template

Basic logging setup with sensible defaults:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Use it
logger.info("Process started")
logger.error("Something went wrong")
```

**When to use**: Any Python script needing basic logging
**Variations**:
- For file logging: Add `filename='app.log'` to basicConfig
- For JSON logs: Use `python-json-logger` package
```

---

## 6. Progressive Disclosure Principle

### What Goes Where?

**SKILL.md** (< 500 lines)
- Quickstart (how to get started fast)
- Workflow (decision points, main algorithm)
- Guardrails (what it can/cannot do)
- 2+ templates (practical examples)
- 5+ failure modes
- 3+ edge cases
- References navigation

**references/** (unlimited)
- Extended examples
- Detailed troubleshooting
- Related skills
- Internal standards/constraints
- Change history
- Performance considerations

**scripts/** (as needed)
- Automated, deterministic operations
- Complex logic that shouldn't be in SKILL.md
- Reusable utilities

### The "Desk Test"
Can someone learn to use the skill by reading SKILL.md in 5-10 minutes? If not, too much content in SKILL.md.

---

## 7. Handling Conflicts

When external best practices conflict with your constraints:

### Priority Order
1. **Compliance/org red lines** - Never violated
2. **User preferences** - Usually followed
3. **External best practices** - Used as defaults

### Document Conflicts Explicitly

```markdown
## Default Approach (External Best Practice)
Use async/await for performance

## Our Approach (Local Constraint)
Use synchronous code for simplicity and debuggability
Tradeoff: ~10% slower but much easier to understand
```

---

## 8. Skill Naming Conventions

### Pattern: `[domain]-[action]`

✅ **Good**
- `python-linting`
- `api-documentation`
- `data-validation`
- `git-workflow`

❌ **Bad**
- `skill123`
- `my-tool`
- `stuff`

---

## 9. Red Flags When Building

| Red Flag | What It Means | What To Do |
|----------|---------------|-----------|
| Can't clearly state "what this does" in 1 sentence | Scope too broad | Split into 2+ skills |
| Failure modes list is generic (just "error handling") | Insufficient thought | Deep-dive on real failure scenarios |
| Can't think of 3+ edge cases | Too simple or over-specified | Redefine scope or consider templates |
| Triggers all similar | Redundant | Diversify entry points |
| SKILL.md already at 500 lines in draft | Too much content | Move details to references/ |

---

## 10. Testing Your Skill

### Can Someone Else Use It?
- Give the SKILL.md to a colleague unfamiliar with the topic
- Can they successfully use the skill in 10 minutes?
- Do they hit any failure modes?
- Are the templates actually helpful?

### Does It Handle Edge Cases?
- Try with empty input
- Try with maximum input (large files, many items)
- Try on different OS/environment
- Try with non-ASCII characters

### Is It Maintainable?
- Can someone update it in 6 months?
- Are decision points clear?
- Are the failure modes still relevant?

---

## Quick Checklist

Before declaring a skill "done":

- [ ] Goal is clear and achievable
- [ ] 5+ distinct trigger phrases
- [ ] 3+ must-cover, 3+ must-not-cover items
- [ ] Output format is specific and realistic
- [ ] Quickstart is 3-5 steps and <100 words
- [ ] 2+ practical, copy-paste-able templates
- [ ] 5+ failure modes with root causes and fixes
- [ ] 3+ edge cases identified and addressed
- [ ] Guardrails clearly state boundaries
- [ ] SKILL.md < 500 lines
- [ ] References section helps users find more
- [ ] Formatting is consistent (bold, code blocks, lists)
- [ ] Spelling and grammar checked
- [ ] A colleague can use it without your help
