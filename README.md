# SkillForge - AI Skill Generator

🛠️ **Automated skill generation powered by NotebookLM + Claude pipeline**

Transform any requirement into a production-ready SKILL.md file following skill-creator standards.

## What SkillForge Does

SkillForge automates the creation of reusable skills by:

1. **Guiding you through scope definition** - Clarify your skill's goal, triggers, coverage
2. **Gathering external best practices** - Leveraging NotebookLM for knowledge synthesis
3. **Collecting your constraints** - Understanding organization-specific requirements
4. **Auto-generating SKILL.md** - Compiling all inputs into a professional skill file
5. **Validating quality** - Ensuring all quality gates are met

## Quick Start (3 Steps)

### Step 1: Describe Your Skill

```bash
cd scripts/
python skillforge_engine.py "make a skill for Python linting"
```

This will guide you through:
- Defining your skill's goal
- Listing trigger phrases (5+)
- Specifying coverage (must cover 3+, must not cover 3+)
- Selecting output format

### Step 2: Answer Quick Questions

SkillForge will ask 5 questions about your constraints:

1. Compliance/org requirements?
2. Required/forbidden tools?
3. Output format specifications?
4. Your priority (speed/accuracy/explainability/consistency)?
5. Known failure patterns?

### Step 3: Review Generated Skill

The generated skill includes:

- **SKILL.md** - Production-ready skill file
- **metadata.json** - Generation details and validation report
- **References** - Best practices, templates, examples

## Architecture: 6-Step Process

```
┌────────────────────────────────────────────────────────────┐
│ Step 1: SCOPE CARD                                          │
│ ├─ Goal, triggers, coverage                                 │
│ └─ Degrees of freedom analysis                              │
├────────────────────────────────────────────────────────────┤
│ Step 3: EXTERNAL CANON (NotebookLM)                         │
│ ├─ Auto-create notebook from scope                          │
│ ├─ Ask structured questions                                 │
│ └─ Extract best practices                                   │
├────────────────────────────────────────────────────────────┤
│ Step 5: LOCAL OVERLAY (User Interview)                      │
│ ├─ Compliance constraints                                   │
│ ├─ Tool preferences                                         │
│ └─ Known failure patterns                                   │
├────────────────────────────────────────────────────────────┤
│ Step 6: SKILL COMPILATION                                   │
│ ├─ Merge canon + overlay                                    │
│ ├─ Resolve conflicts                                        │
│ └─ Generate SKILL.md                                        │
├────────────────────────────────────────────────────────────┤
│ QUALITY GATES                                               │
│ ├─ Description clarity                                      │
│ ├─ Quickstart executable (30s)                              │
│ ├─ 2+ templates                                             │
│ ├─ 5+ failure modes                                         │
│ ├─ 3+ edge cases                                            │
│ ├─ Brittle tasks scripted                                   │
│ └─ SKILL.md < 500 lines                                     │
└────────────────────────────────────────────────────────────┘
```

## Project Structure

```
skillforge/
├── SKILL.md                    # Original SkillForge documentation
├── README.md                   # This file
├── agents/
│   └── openai.yaml            # UI configuration
├── scripts/
│   ├── skillforge_engine.py    # Main orchestration engine (220 lines)
│   ├── skill_compiler.py       # Compilation engine (360 lines)
│   ├── notebooklm_integration.py # NotebookLM bridge (180 lines)
│   ├── scope_card_builder.py   # Step 1: Scope card (160 lines)
│   ├── user_interview.py       # Step 5: User constraints (170 lines)
│   ├── validators.py           # Quality gates (300 lines)
│   └── __init__.py
├── references/
│   ├── skill_templates.md      # 6 common skill patterns
│   ├── best_practices.md       # How to write excellent skills
│   ├── user_overrides_template.md # Constraint template
│   └── examples.md             # Real skill examples (coming)
└── data/
    └── .gitignore             # Protect generated artifacts
```

## Core Modules

### skillforge_engine.py (Main Entry Point)
**Responsibility**: Orchestrate the entire 6-step process

```python
engine = SkillForgeEngine()
result = await engine.generate_skill("make a skill for X")
```

### skill_compiler.py (Core Logic)
**Responsibility**: Compile external canon + local overlay → SKILL.md

Key conflicts resolution:
1. Compliance/org constraints (highest priority)
2. User preferences
3. External best practices (fallback)

### notebooklm_integration.py (Knowledge Source)
**Responsibility**: Integrate with NotebookLM for external knowledge

Collects structured answers about:
- Quickstart procedures
- Decision points
- Templates and examples
- Failure modes and fixes
- Edge cases

### scope_card_builder.py (Interactive Guide)
**Responsibility**: Guide user through Step 1 - defining scope

Validates:
- 1-sentence goal (min 10 chars)
- 5+ trigger phrases
- 3+ must-cover items
- 3+ must-not-cover items
- Clear output format
- Measurable success criteria

### user_interview.py (Constraint Collector)
**Responsibility**: Conduct Step 5 - collect organizational constraints

5 key questions:
1. Compliance/red lines
2. Tool requirements
3. Output format specs
4. Priority (speed/accuracy/explainability/consistency)
5. Known failure patterns

### validators.py (Quality Gates)
**Responsibility**: Ensure quality standards are met

7 gates:
- [ ] Description clarity
- [ ] Quickstart executable (30s)
- [ ] 2+ templates
- [ ] 5+ failure modes
- [ ] 3+ edge cases
- [ ] Brittle tasks scripted
- [ ] File size < 500 lines

## Configuration

### Environment Variables

```bash
# Choose NotebookLM integration mode
SKILLFORGE_MODE=auto|manual     # Default: auto

# Logging
SKILLFORGE_LOG_LEVEL=DEBUG|INFO|WARNING|ERROR

# Output location
SKILLFORGE_OUTPUT_DIR=./skillforge_output
```

### Custom Constraints Template

See `references/user_overrides_template.md` for organization-specific constraint format.

## Usage Patterns

### Interactive Mode (Default)
```bash
python scripts/skillforge_engine.py "your skill idea"
# Will prompt for all inputs
```

### Scripted Mode
```bash
# Pre-define scope card in JSON
python scripts/skillforge_engine.py --scope-file scope.json
```

### Programmatic Mode
```python
from scripts import SkillForgeEngine

engine = SkillForgeEngine(storage_dir="/output")
result = await engine.generate_skill(
    "make a skill for X",
    interactive=False  # Use defaults
)
```

## Generated Skill Output

When generation completes, you get:

```
skillforge_output/
└── skill_20240203_123456/
    ├── SKILL.md                           # Ready to use!
    ├── metadata.json                      # Generation details
    ├── references/
    │   ├── user_overrides.md             # Your constraints
    │   ├── templates.md                  # Extracted templates
    │   └── examples.md                   # Real examples
    └── scripts/
        └── [optional automation scripts]
```

## Quality Checklist

Every generated skill passes:

```
✓ Clear, specific description with triggers
✓ 30-second quickstart (3-5 steps)
✓ 2+ practical, copy-paste-able templates
✓ 5+ failure modes with solutions
✓ 3+ identified edge cases
✓ Clear guardrails (what it does/doesn't do)
✓ < 500 lines in SKILL.md
✓ Clear references navigation
```

## Troubleshooting

### "How do I add more templates?"
Edit the generated skill's SKILL.md - add more ### Template sections

### "The generated skill isn't perfect"
SkillForge creates a solid foundation. You can:
1. Edit SKILL.md directly
2. Add custom scripts/ directory
3. Expand references/ with more examples

### "How do I update an existing skill?"
Re-run SkillForge with the same request - it will use your previous answers as defaults.

## Learning Resources

- **Quick patterns**: See `references/skill_templates.md`
- **Best practices**: See `references/best_practices.md`
- **Real examples**: See `references/examples.md` (being populated)
- **Original guide**: See the existing SKILL.md in this directory

## Success Metrics

A successful SkillForge run produces a skill where:

- ✓ Someone unfamiliar with the topic can use it in <10 minutes
- ✓ Covers 3+ realistic scenarios
- ✓ Handles all documented failure modes gracefully
- ✓ Ready to commit to production (with optional org customizations)

## Contributing Back

If you create an excellent skill using SkillForge:
1. Add it to `references/examples.md`
2. Share the scope card - helps improve templates
3. Report any quality gate failures

## Limitations

Current version:
- Requires NotebookLM access (gracefully fallbacks to offline mode)
- SKILL.md automation focuses on content structure, not perfect English
- Edge case detection requires domain knowledge (best effort)
- Quality gates are guidelines, not absolute requirements

## Next Steps

1. **Try it**: `python scripts/skillforge_engine.py "your idea"`
2. **Review**: Check the generated SKILL.md and metadata
3. **Customize**: Edit as needed for your org
4. **Deploy**: Use the skill in production
5. **Share**: Add to references/examples.md

---

**SkillForge v1.0** | Powered by NotebookLM + skill-creator standards
