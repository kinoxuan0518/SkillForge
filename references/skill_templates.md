# Skill Templates Library

This document provides templates for common skill patterns that SkillForge can help you create.

## Template 1: Text Processing Skill

### Use When
- Transforming text, parsing, extracting information
- Formatting conversions (markdown → HTML, CSV → JSON)
- Content analysis and classification

### Scope Card Template
```
Goal: Transform/analyze text in specific ways
Must Cover: Common text formats (input/output), edge cases
Must Not Cover: Binary data, images, audio
Output Form: Template/Script
Success Criteria: Correct transformation, handles edge cases
```

### Typical Sections
- Quickstart: Parse, Transform, Validate
- Decision points: Input format? Preserve formatting?
- Failure modes: Encoding issues, special characters, empty input
- Edge cases: Non-ASCII characters, very long text, malformed input

---

## Template 2: CLI Tool / Command Skill

### Use When
- Wrapping existing command-line tools
- Automating common terminal tasks
- Building developer utilities

### Scope Card Template
```
Goal: Simplify usage of a complex CLI tool
Must Cover: Common use cases, option combinations
Must Not Cover: Advanced/rare flags, GUI mode
Output Form: Script/Commands
Success Criteria: Runs without errors, produces expected output
```

### Typical Sections
- Quickstart: Install, Configure, Run
- Decision points: Which command variant? Which options?
- Failure modes: Path not found, permission denied, version mismatch
- Edge cases: Missing dependencies, different OS behavior

---

## Template 3: Decision Tree / Workflow Skill

### Use When
- Guiding complex decision-making processes
- Troubleshooting workflows
- Multi-step procedures with branches

### Scope Card Template
```
Goal: Guide user through decision process
Must Cover: Main decision branches, each outcome
Must Not Cover: Out-of-scope decisions, expert-only cases
Output Form: Decision Tree / Flowchart
Success Criteria: User reaches correct decision/outcome
```

### Typical Sections
- Quickstart: Gather inputs, Follow tree, Apply decision
- Decision points: If X then Y, Otherwise Z (3+ branches)
- Failure modes: Ambiguous inputs, edge case conflicts, user stuck
- Edge cases: Inputs don't fit tree, conflicting goals

---

## Template 4: API Integration Skill

### Use When
- Integrating with external APIs
- Authentication and data retrieval flows
- Rate limiting and error handling

### Scope Card Template
```
Goal: Simplify interaction with API
Must Cover: Common endpoints, auth methods, error handling
Must Not Cover: Advanced features, custom implementations
Output Form: Template/Script
Success Criteria: Can make API calls, get expected responses
```

### Typical Sections
- Quickstart: Authenticate, Make Request, Parse Response
- Decision points: Which endpoint? Which auth method?
- Failure modes: Auth failure, rate limit hit, API changes, network errors
- Edge cases: Empty responses, pagination, timeout

---

## Template 5: Data Validation Skill

### Use When
- Checking data quality, format compliance
- Pre-processing validation
- Schema enforcement

### Scope Card Template
```
Goal: Validate data meets specified requirements
Must Cover: Format checks, value ranges, dependencies
Must Not Cover: Performance optimization, large-scale processing
Output Form: Template/Checklist
Success Criteria: All invalid data detected and flagged
```

### Typical Sections
- Quickstart: Define rules, Check data, Report issues
- Decision points: Which validation type? Strictness level?
- Failure modes: False positives/negatives, missing edge cases
- Edge cases: Null values, type mismatches, unicode

---

## Template 6: Configuration / Setup Skill

### Use When
- Multi-step setup procedures
- Configuration best practices
- Initialization workflows

### Scope Card Template
```
Goal: Guide through configuration/setup
Must Cover: Required steps, best practices, validation
Must Not Cover: Troubleshooting existing configurations
Output Form: Template/Checklist
Success Criteria: System configured and verified working
```

### Typical Sections
- Quickstart: Gather inputs, Apply config, Verify
- Decision points: Which setup variant? Optional features?
- Failure modes: Missing prerequisites, permission issues, conflicts
- Edge cases: Existing partial config, version mismatches

---

## Common Failure Mode Patterns

### Symptom: "It worked before but not now"
**Fix**: Version mismatch, environment change, API deprecation

### Symptom: "Works on my machine but not others"
**Fix**: Environment-specific (OS, packages, paths, permissions)

### Symptom: "Works but produces unexpected output"
**Fix**: Input format different than expected, missing edge case handling

### Symptom: "Runs too slowly"
**Fix**: Inefficient approach, missing optimization, resource constraints

### Symptom: "Error with special characters / non-ASCII"
**Fix**: Encoding issues, character handling, locale-specific behavior

---

## Common Edge Cases by Category

### Text Processing
- Empty input
- Very long input (>1MB)
- Non-ASCII characters (emoji, accents)
- Special characters that need escaping
- Mixed line endings (CRLF vs LF)

### CLI Tools
- Tool not in PATH
- Wrong version installed
- Different behavior across OS (Windows/Mac/Linux)
- Different shell environments (bash/zsh/fish)
- Path spaces and special characters

### APIs
- Empty/null responses
- Pagination for large result sets
- Rate limiting (429 Too Many Requests)
- Timeout on slow networks
- Version deprecation

### Workflows
- Partially completed workflows
- Conflicting configuration options
- Missing or invalid prerequisites
- User goes "off the happy path"
- Ambiguous user input

---

## Quality Checklist for Your Skill

- [ ] Description is clear about triggers and scope
- [ ] Quickstart is 3-5 steps, doable in 30 seconds
- [ ] 2+ practical templates/examples with code
- [ ] 5+ documented failure modes with fixes
- [ ] 3+ edge cases identified and addressed
- [ ] Guardrails clearly state what it CAN and CANNOT do
- [ ] SKILL.md is <500 lines (detailed content in references/)
- [ ] References navigation helps users find more info

