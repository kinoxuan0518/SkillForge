"""
Skill Validators - Quality Gates for SkillForge

Enforces the 7 quality gates from SkillForge Step 6:
1. Description clarity (triggers + scope)
2. Quickstart executable (30 seconds)
3. 2+ templates
4. 5+ failure modes with fixes
5. 3+ edge cases
6. Brittle tasks scripted
7. SKILL.md < 500 lines
"""

import logging
import re
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)


class QualityGate:
    """Represents a quality gate check."""

    def __init__(self, name: str, category: str, required: bool = True):
        self.name = name
        self.category = category  # mandatory/recommended/nice-to-have
        self.required = required

    def check(self, *args, **kwargs) -> Tuple[bool, str]:
        """Check gate and return (passed, message)."""
        raise NotImplementedError


class SkillValidator:
    """
    Validates generated skills against quality gates.

    Returns detailed validation report with:
    - Gate status (pass/fail/warn)
    - Specific issues found
    - Recommendations
    """

    def __init__(self):
        """Initialize validator with all quality gates."""
        self.gates = []
        self._setup_gates()

    def _setup_gates(self) -> None:
        """Set up all quality gates."""
        self.gates = [
            self.DescriptionGate(),
            self.QuickstartGate(),
            self.TemplatesGate(),
            self.FailureModesGate(),
            self.EdgeCasesGate(),
            self.BrittlenessGate(),
            self.SizeGate(),
        ]

    def validate_skill(self, skill_md: str, scope_card: Dict, canon: Dict) -> Dict:
        """
        Run all quality gates on a skill.

        Args:
            skill_md: Generated SKILL.md content
            scope_card: Step 1 scope card
            canon: Step 3 external canon

        Returns:
            Validation report dict
        """
        logger.info("Running quality gates...")

        report = {
            "passed": True,
            "gates": [],
            "errors": [],
            "warnings": [],
            "recommendations": [],
        }

        for gate in self.gates:
            passed, message, details = gate.validate(skill_md, scope_card, canon)

            gate_result = {
                "name": gate.name,
                "category": gate.category,
                "passed": passed,
                "message": message,
                "required": gate.required,
            }

            report["gates"].append(gate_result)

            if not passed:
                if gate.required:
                    report["errors"].append(message)
                    report["passed"] = False
                else:
                    report["warnings"].append(message)

            # Collect recommendations
            if "recommendation" in details:
                report["recommendations"].append(details["recommendation"])

            logger.info(f"  Gate '{gate.name}': {'✓' if passed else '✗'}")

        return report

    def print_report(self, report: Dict) -> None:
        """Print validation report in readable format."""
        print("\n" + "="*60)
        print("QUALITY GATES VALIDATION REPORT")
        print("="*60 + "\n")

        # Overall status
        if report["passed"]:
            print("✓ ALL GATES PASSED\n")
        else:
            print("✗ SOME GATES FAILED\n")

        # Gate details
        for gate in report["gates"]:
            status = "✓" if gate["passed"] else "✗"
            required = "[REQUIRED]" if gate["required"] else "[Optional]"
            print(f"{status} {gate['name']} {required}")
            print(f"   {gate['message']}\n")

        # Errors (if any)
        if report["errors"]:
            print("\nERRORS (must fix):")
            for error in report["errors"]:
                print(f"  ✗ {error}")

        # Warnings (if any)
        if report["warnings"]:
            print("\nWARNINGS (should fix):")
            for warning in report["warnings"]:
                print(f"  ⚠ {warning}")

        # Recommendations
        if report["recommendations"]:
            print("\nRECOMMENDATIONS:")
            for rec in report["recommendations"]:
                print(f"  → {rec}")

        print("\n" + "="*60 + "\n")

    # Gate implementations
    class DescriptionGate(QualityGate):
        """Gate 1: Description clarity."""

        def __init__(self):
            super().__init__("Description Clarity", "mandatory", required=True)

        def validate(self, skill_md: str, scope_card: Dict, canon: Dict) -> Tuple[bool, str, Dict]:
            """Check if frontmatter has clear description."""
            issues = []

            # Extract frontmatter
            match = re.match(r'^---\n(.*?)\n---', skill_md, re.DOTALL)
            if not match:
                return False, "Missing YAML frontmatter", {}

            frontmatter = match.group(1)

            # Check name
            if "name:" not in frontmatter:
                issues.append("No name field in frontmatter")

            # Check description
            desc_match = re.search(r'description:\s*(.+?)(?:\n|$)', frontmatter)
            if not desc_match:
                issues.append("No description field in frontmatter")
            else:
                desc = desc_match.group(1)
                if len(desc) < 50:
                    issues.append("Description too short (< 50 chars)")

            passed = len(issues) == 0
            message = ", ".join(issues) if issues else "✓ Clear frontmatter with name and description"

            return passed, message, {}

    class QuickstartGate(QualityGate):
        """Gate 2: Quickstart executable in 30 seconds."""

        def __init__(self):
            super().__init__("Quickstart (30s)", "mandatory", required=True)

        def validate(self, skill_md: str, scope_card: Dict, canon: Dict) -> Tuple[bool, str, Dict]:
            """Check if Quickstart section exists and is concise."""
            if "## Quick Start" not in skill_md and "## Quickstart" not in skill_md:
                return False, "No Quickstart section found", {}

            # Extract Quickstart
            match = re.search(r'## Quick[Ss]tart\n\n(.*?)(?:\n## |\nZ)', skill_md + "\nZ", re.DOTALL)
            if not match:
                return False, "Quickstart section empty", {}

            quickstart = match.group(1)
            lines = [l.strip() for l in quickstart.split("\n") if l.strip()]

            if len(lines) > 5:
                return False, f"Quickstart too long ({len(lines)} items, max 3-4)", {
                    "recommendation": "Simplify to 3 clear steps"
                }

            return True, "✓ Concise 30-second quickstart", {}

    class TemplatesGate(QualityGate):
        """Gate 3: 2+ templates."""

        def __init__(self):
            super().__init__("Templates (≥2)", "mandatory", required=True)

        def validate(self, skill_md: str, scope_card: Dict, canon: Dict) -> Tuple[bool, str, Dict]:
            """Check for template examples."""
            template_section = re.search(r'## Templates.*?\n\n(.*?)(?:\n## |\nZ)', skill_md + "\nZ", re.DOTALL)

            if not template_section:
                return False, "No Templates section found", {}

            # Count code blocks
            code_blocks = len(re.findall(r'```', skill_md))

            if code_blocks < 2:
                return False, f"Found {code_blocks} code examples, need ≥2", {
                    "recommendation": "Add template examples and code samples"
                }

            return True, f"✓ {code_blocks} template examples found", {}

    class FailureModesGate(QualityGate):
        """Gate 4: 5+ failure modes with fixes."""

        def __init__(self):
            super().__init__("Failure Modes (≥5)", "mandatory", required=True)

        def validate(self, skill_md: str, scope_card: Dict, canon: Dict) -> Tuple[bool, str, Dict]:
            """Check for comprehensive failure modes."""
            if "## Failure" not in skill_md:
                return False, "No Failure Modes section found", {}

            # Count failure mode entries
            # Look for "Symptom:" or "- **" patterns
            failures = len(re.findall(r'\*\*(?:Symptom|Symptom|Failure|Issue):', skill_md))

            if failures < 5:
                return False, f"Only {failures} failure modes found, need ≥5", {
                    "recommendation": "Add more comprehensive failure mode documentation"
                }

            # Check for fix descriptions
            if "**Fix" not in skill_md and "fix:" not in skill_md.lower():
                return False, "Failure modes lack fix/solution descriptions", {}

            return True, f"✓ {failures}+ failure modes with solutions", {}

    class EdgeCasesGate(QualityGate):
        """Gate 5: 3+ edge cases."""

        def __init__(self):
            super().__init__("Edge Cases (≥3)", "mandatory", required=True)

        def validate(self, skill_md: str, scope_card: Dict, canon: Dict) -> Tuple[bool, str, Dict]:
            """Check for edge cases."""
            if "## Edge" not in skill_md:
                return False, "No Edge Cases section found", {}

            # Count edge cases (- bullet points after Edge Cases header)
            match = re.search(r'## Edge Cases\n\n(.*?)(?:\n## |\nZ)', skill_md + "\nZ", re.DOTALL)

            if not match:
                return False, "Edge Cases section empty", {}

            edge_cases = re.findall(r'^-\s+', match.group(1), re.MULTILINE)

            if len(edge_cases) < 3:
                return False, f"Only {len(edge_cases)} edge cases found, need ≥3", {
                    "recommendation": "Document boundary conditions and unusual scenarios"
                }

            return True, f"✓ {len(edge_cases)} edge cases documented", {}

    class BrittlenessGate(QualityGate):
        """Gate 6: Brittle tasks scripted."""

        def __init__(self):
            super().__init__("Brittle Tasks Scripted", "recommended", required=False)

        def validate(self, skill_md: str, scope_card: Dict, canon: Dict) -> Tuple[bool, str, Dict]:
            """Check if brittle tasks have scripts."""
            # Look for guardrails or scripts section
            has_guardrails = "## Guardrails" in skill_md
            has_scripts = "scripts/" in skill_md

            if has_scripts:
                return True, "✓ Scripts provided for brittle operations", {}
            elif has_guardrails:
                return True, "✓ Guardrails clearly documented", {}
            else:
                return False, "No explicit guardrails or scripts for brittle tasks", {
                    "recommendation": "Add scripts or strict guardrails for error-prone steps"
                }

    class SizeGate(QualityGate):
        """Gate 7: SKILL.md < 500 lines."""

        def __init__(self):
            super().__init__("File Size (<500 lines)", "recommended", required=False)

        def validate(self, skill_md: str, scope_card: Dict, canon: Dict) -> Tuple[bool, str, Dict]:
            """Check file size."""
            lines = len(skill_md.split("\n"))

            if lines > 600:
                return False, f"SKILL.md is {lines} lines, should be <500", {
                    "recommendation": "Move detailed content to references/ directory"
                }
            elif lines > 500:
                return False, f"SKILL.md is {lines} lines, aim for <500", {
                    "recommendation": "Consider moving some content to references/"
                }

            return True, f"✓ Concise at {lines} lines", {}
