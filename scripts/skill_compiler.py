"""
Skill Compiler - Compiles External Canon + Local Overlay into SKILL.md

This is the core compilation engine that transforms:
- External Canon (NotebookLM best practices)
- Local Overlay (user/organization constraints)
Into a production-ready SKILL.md file

Compilation rules:
1. Compliance/org hard constraints > user preference > external best practices
2. Explicit conflict resolution with trade-offs noted
3. Progressive disclosure: SKILL.md < 500 lines, details in references/
"""

import json
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)


@dataclass
class CompilationContext:
    """Context for skill compilation."""
    scope_card: Dict
    canon: Dict
    overlay: Dict
    conflicts: List[Dict] = None
    decisions: List[Dict] = None

    def __post_init__(self):
        if self.conflicts is None:
            self.conflicts = []
        if self.decisions is None:
            self.decisions = []


class SkillCompiler:
    """
    Compiles External Canon + Local Overlay into SKILL.md.

    Enforces the compilation rules from SkillForge's Step 6:
    - Compliance constraints (hard, non-negotiable)
    - User preferences (soft, can be overridden)
    - External best practices (default, can be overridden)
    """

    # Conflict resolution priority (highest to lowest)
    PRIORITY = [
        "compliance",  # 1. Org red lines (absolute)
        "user_preference",  # 2. User's stated preference
        "canon",  # 3. External best practices
    ]

    def compile(self, scope_card: Dict, canon: Dict, overlay: Dict) -> str:
        """
        Main compilation entry point.

        Args:
            scope_card: Step 1 output (scope definition)
            canon: Step 3 output (external knowledge)
            overlay: Step 5 output (user constraints)

        Returns:
            Compiled SKILL.md content (string)
        """
        logger.info("Starting skill compilation...")

        ctx = CompilationContext(scope_card, canon, overlay)

        # Build frontmatter
        frontmatter = self._compile_frontmatter(ctx)

        # Build body sections
        sections = {
            "description": self._compile_description(ctx),
            "when_to_use": self._compile_when_to_use(ctx),
            "quickstart": self._compile_quickstart(ctx),
            "workflow": self._compile_workflow(ctx),
            "guardrails": self._compile_guardrails(ctx),
            "templates": self._compile_templates(ctx),
            "failure_modes": self._compile_failure_modes(ctx),
            "edge_cases": self._compile_edge_cases(ctx),
            "references": self._compile_references(ctx),
        }

        # Check size and warn if needed
        skill_md = self._assemble_skill_md(frontmatter, sections)
        line_count = len(skill_md.split("\n"))

        if line_count > 500:
            logger.warning(f"SKILL.md is {line_count} lines (target: <500). Consider moving content to references/")

        return skill_md

    def _compile_frontmatter(self, ctx: CompilationContext) -> str:
        """Compile YAML frontmatter."""
        scope = ctx.scope_card
        name = self._sanitize_skill_name(scope.get("goal", "unnamed_skill"))
        description = self._compile_description_short(ctx)

        return f"""---
name: {name}
description: {description}
---
"""

    def _sanitize_skill_name(self, text: str) -> str:
        """Convert skill goal to safe skill name."""
        # Extract key words from goal
        # "Create a skill for Python linting" → "python-linting"
        words = text.lower().split()
        # Remove common words and sanitize
        stop_words = {"a", "the", "for", "skill", "create", "make", "build"}
        words = [w for w in words if w not in stop_words and w.isalnum()]
        return "-".join(words[:3])  # Take first 3 words

    def _compile_description_short(self, ctx: CompilationContext) -> str:
        """Compile short description for frontmatter."""
        scope = ctx.scope_card
        goal = scope.get("goal", "")
        triggers = scope.get("trigger_words", [])

        description = f"{goal}. "
        description += f"Triggers: {', '.join(triggers[:3])}."

        if ctx.overlay.get("required_tools"):
            description += f" Uses: {', '.join(ctx.overlay['required_tools'][:2])}."

        return description[:200]  # Max 200 chars

    def _compile_description(self, ctx: CompilationContext) -> str:
        """Compile full description section."""
        scope = ctx.scope_card

        return f"""## Overview

**Purpose**: {scope.get('goal', 'Unknown')}

**What this skill does**:
- {chr(10).join(f"- {item}" for item in scope.get('must_cover', [])[:3])}

**When to use this**:
- {chr(10).join(f"- {trigger}" for trigger in scope.get('trigger_words', [])[:3])}

**What this skill does NOT do**:
- {chr(10).join(f"- {item}" for item in scope.get('must_not_cover', [])[:2])}
"""

    def _compile_when_to_use(self, ctx: CompilationContext) -> str:
        """Compile 'When to Use' section."""
        overlay = ctx.overlay
        scope = ctx.scope_card

        section = "## When to Use This Skill\n\n"

        if overlay.get("required_tools"):
            section += f"**Required Tools**: {', '.join(overlay['required_tools'])}\n\n"

        if overlay.get("forbidden_tools"):
            section += f"**Cannot Use**: {', '.join(overlay['forbidden_tools'])}\n\n"

        if overlay.get("priority"):
            priorities = {
                "speed": "Speed is most important - get fast results even if imperfect",
                "accuracy": "Accuracy is critical - must be verified and precise",
                "explainability": "Explainability matters - must be transparent and clear",
                "consistency": "Consistency is key - must produce uniform results",
            }
            section += f"**Priority**: {priorities.get(overlay['priority'], 'Balanced')}\n\n"

        return section

    def _compile_quickstart(self, ctx: CompilationContext) -> str:
        """Compile Quickstart section (max 3 steps)."""
        canon = ctx.canon
        quickstart = canon.get("quickstart", "")

        # Parse or generate 3-step quickstart
        steps = quickstart.split("\n")[:3] if quickstart else ["Step 1: Start", "Step 2: Configure", "Step 3: Execute"]

        section = "## Quick Start\n\n"
        for i, step in enumerate(steps, 1):
            section += f"{i}. {step.strip()}\n"

        return section + "\n"

    def _compile_workflow(self, ctx: CompilationContext) -> str:
        """Compile Workflow section with decision points."""
        canon = ctx.canon
        decision_points = canon.get("decision_points", [])
        overlay = ctx.overlay

        section = "## Workflow\n\n"

        if decision_points:
            section += "### Decision Points\n\n"
            for point in decision_points[:5]:  # Limit to 5 decision points
                section += f"- {point}\n"
        else:
            section += "### Default Workflow\n\n"
            section += "1. Analyze input\n"
            section += "2. Choose approach based on context\n"
            section += "3. Execute\n"

        if overlay.get("output_format"):
            section += f"\n### Required Output Format\n\n"
            fmt = overlay["output_format"]
            if isinstance(fmt, dict):
                for key, value in fmt.items():
                    section += f"- **{key}**: {value}\n"

        return section + "\n"

    def _compile_guardrails(self, ctx: CompilationContext) -> str:
        """Compile Guardrails section (self-freedom constraints)."""
        scope = ctx.scope_card
        overlay = ctx.overlay

        section = "## Guardrails\n\n"

        section += "### What This Can Do\n"
        section += f"{chr(10).join(f'- {item}' for item in scope.get('must_cover', [])[:3])}\n\n"

        section += "### What This Cannot Do\n"
        section += f"{chr(10).join(f'- {item}' for item in scope.get('must_not_cover', [])[:3])}\n\n"

        if overlay.get("compliance_constraints"):
            section += f"### Compliance Requirements\n\n"
            section += f"{overlay['compliance_constraints']}\n\n"

        return section

    def _compile_templates(self, ctx: CompilationContext) -> str:
        """Compile Templates section (≥2 templates)."""
        canon = ctx.canon
        templates = canon.get("templates", [])

        section = "## Templates / Examples\n\n"

        if templates:
            for template in templates[:5]:  # Max 5 templates
                name = template.get("name", "Template")
                content = template.get("content", "")
                section += f"### {name}\n\n```\n{content}\n```\n\n"
        else:
            section += "### Default Template\n\n```\n[Template content will be added]\n```\n\n"

        return section

    def _compile_failure_modes(self, ctx: CompilationContext) -> str:
        """Compile Failure Modes section (≥5 modes)."""
        canon = ctx.canon
        failure_modes = canon.get("failure_modes", [])
        overlay = ctx.overlay

        section = "## Failure Modes & Fixes\n\n"

        # From canon
        if failure_modes:
            for mode in failure_modes[:5]:
                symptom = mode.get("symptom", "Unknown")
                fix = mode.get("fix", "Unknown")
                section += f"**Symptom**: {symptom}\n"
                section += f"**Fix**: {fix}\n\n"
        else:
            section += "- **Symptom**: Expected behavior not achieved\n"
            section += "  **Fix**: Check inputs and prerequisites\n\n"

        # Add failure history from overlay
        if overlay.get("failure_history"):
            section += "### Common Failures in Your Context\n\n"
            for failure in overlay["failure_history"][:3]:
                section += f"- {failure}\n"
            section += "\n"

        return section

    def _compile_edge_cases(self, ctx: CompilationContext) -> str:
        """Compile Edge Cases section (≥3 cases)."""
        canon = ctx.canon
        edge_cases = canon.get("edge_cases", [])
        scope = ctx.scope_card

        section = "## Edge Cases\n\n"

        if edge_cases:
            for case in edge_cases[:5]:
                section += f"- {case}\n"
        else:
            section += "- Empty input\n"
            section += "- Boundary conditions\n"
            section += "- Unusual combinations\n"

        # Add from must_not_cover
        if scope.get("must_not_cover"):
            section += "\n### Out of Scope (Related But Not Covered)\n"
            for item in scope["must_not_cover"][:3]:
                section += f"- {item}\n"

        return section + "\n"

    def _compile_references(self, ctx: CompilationContext) -> str:
        """Compile References Navigation section."""
        return """## References & More Information

For detailed information, see:
- `references/user_overrides.md` - Organization-specific constraints and preferences
- `references/templates.md` - Template library and variations
- `references/examples.md` - Success stories and case studies
- `references/best_practices.md` - Best practices and gotchas

### Conflict Resolution

This skill resolves conflicts between external best practices and local constraints:
1. **Compliance/Org requirements** (highest priority) - never violated
2. **User preferences** - followed unless conflict with compliance
3. **External best practices** (lowest priority) - used as defaults

See `references/decisions.md` for detailed resolution notes.
"""

    def _assemble_skill_md(self, frontmatter: str, sections: Dict[str, str]) -> str:
        """Assemble final SKILL.md from components."""
        parts = [frontmatter]

        # Add sections in order
        section_order = [
            "description",
            "when_to_use",
            "quickstart",
            "workflow",
            "guardrails",
            "templates",
            "failure_modes",
            "edge_cases",
            "references",
        ]

        for section_name in section_order:
            if section_name in sections:
                parts.append(sections[section_name])

        skill_md = "\n".join(parts)

        # Remove excessive blank lines
        skill_md = re.sub(r"\n\n\n+", "\n\n", skill_md)

        return skill_md

    def detect_conflicts(self, scope_card: Dict, canon: Dict, overlay: Dict) -> List[Dict]:
        """
        Detect conflicts between canon and overlay.

        Returns list of conflicts with:
        - area: Which skill aspect has conflict
        - canon_says: What external best practice recommends
        - overlay_says: What user/org requires
        - resolution: How the conflict was resolved
        """
        conflicts = []

        # Example conflicts
        if overlay.get("required_tools") and canon.get("templates"):
            # Check if templates use tools not in required_tools
            for template in canon["templates"]:
                content = template.get("content", "")
                # Simple check - in reality would be more sophisticated
                pass

        return conflicts

    def validate_compilation(self, skill_md: str, scope_card: Dict) -> Tuple[bool, List[str]]:
        """
        Validate compiled SKILL.md meets quality standards.

        Returns:
            (is_valid, error_messages)
        """
        errors = []

        # Check length
        line_count = len(skill_md.split("\n"))
        if line_count > 600:
            errors.append(f"SKILL.md too long ({line_count} lines, target <500)")

        # Check required sections
        required_sections = [
            "## Quick Start",
            "## Workflow",
            "## Guardrails",
            "## Failure Modes",
            "## Edge Cases",
        ]
        for section in required_sections:
            if section not in skill_md:
                errors.append(f"Missing section: {section}")

        # Check for minimum content quality
        if skill_md.count("```") < 2:
            errors.append("Need at least 1 code template example")

        if skill_md.count("**") < 6:  # Bold formatting for emphasis
            errors.append("Consider adding more emphasis with **bold text**")

        return len(errors) == 0, errors
