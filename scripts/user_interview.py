"""
User Interview - Step 5 of SkillForge

Collects local constraints and preferences via 5 key questions:
1. Compliance/organizational red lines
2. Required and forbidden tools
3. Output format specifications
4. Priority (speed/accuracy/explainability/consistency)
5. Historical failure patterns
"""

import json
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class UserInterview:
    """Conducts user interview to collect local overlay constraints."""

    QUESTIONS = [
        {
            "id": "compliance",
            "question": "What are your organization's compliance requirements or red lines? (What must NOT happen?)",
            "help": "E.g., 'Cannot use cloud services', 'Must be GDPR compliant', 'Cannot delete data'",
            "parser": lambda ans: ans.strip() if ans else None,
        },
        {
            "id": "tools",
            "question": "Which tools MUST you use? Which are FORBIDDEN?",
            "help": "E.g., 'Must use: PostgreSQL, Python. Cannot use: AWS, JavaScript'",
            "parser": lambda ans: {
                "required": [t.strip() for t in ans.split("Must use:")[-1].split(",")[0].split() if t.strip()],
                "forbidden": [t.strip() for t in ans.split("Cannot use:")[-1].split(",") if t.strip()],
            } if ans else {"required": [], "forbidden": []},
        },
        {
            "id": "format",
            "question": "Is output format fixed? Any specific naming/structure requirements?",
            "help": "E.g., 'Must be JSON with keys: id, name, value', 'Filenames must start with timestamp'",
            "parser": lambda ans: ans.strip() if ans else None,
        },
        {
            "id": "priority",
            "question": "What's your top priority: Speed, Accuracy, Explainability, or Consistency?",
            "help": "Choose ONE: speed (fast, may be imperfect), accuracy (thorough, takes time), explainability (clear reasoning), consistency (uniform results)",
            "parser": lambda ans: ans.strip().lower() if ans else "balanced",
        },
        {
            "id": "failures",
            "question": "What are 3 common failure points in your context?",
            "help": "E.g., 'Timeouts with large files', 'Encoding issues with special characters', 'Memory leaks on long runs'",
            "parser": lambda ans: [f.strip() for f in ans.split("\n") if f.strip()][:3] if ans else [],
        },
    ]

    def __init__(self):
        """Initialize the interviewer."""
        self.overlay = {}

    async def interview(self, scope_card: Dict, interactive: bool = True) -> Dict:
        """
        Conduct user interview.

        Args:
            scope_card: Scope card from Step 1
            interactive: Whether to prompt user

        Returns:
            Local overlay dict
        """
        logger.info("Starting user interview (Step 5)...")

        if interactive:
            return await self._interview_interactive(scope_card)
        else:
            return self._interview_defaults(scope_card)

    async def _interview_interactive(self, scope_card: Dict) -> Dict:
        """Interactive interview mode."""
        print("\n" + "="*60)
        print("SKILLFORGE: USER INTERVIEW (Step 5)")
        print("="*60)
        print("\nWe need to understand your local constraints and preferences.")
        print("These questions should take ~5 minutes.\n")

        overlay = {}

        for i, q_data in enumerate(self.QUESTIONS, 1):
            print(f"\n{i}. {q_data['question']}")
            print(f"   {q_data['help']}")

            answer = input("   > ").strip()

            if not answer:
                print("   [Skipped - will use defaults]")
                answer = self._get_default_answer(q_data["id"])
            else:
                answer = q_data["parser"](answer)

            overlay[q_data["id"]] = answer

        # Validate and summarize
        self._print_interview_summary(overlay)

        return self._structure_overlay(overlay)

    async def _interview_defaults(self, scope_card: Dict) -> Dict:
        """Non-interactive mode: use defaults."""
        logger.info("Using default overlay (non-interactive mode)")

        overlay = {}
        for q_data in self.QUESTIONS:
            overlay[q_data["id"]] = self._get_default_answer(q_data["id"])

        return self._structure_overlay(overlay)

    def _get_default_answer(self, question_id: str) -> any:
        """Get default answer for a question."""
        defaults = {
            "compliance": None,
            "tools": {"required": [], "forbidden": []},
            "format": None,
            "priority": "balanced",
            "failures": [],
        }
        return defaults.get(question_id)

    def _structure_overlay(self, raw_answers: Dict) -> Dict:
        """Structure raw interview answers into overlay format."""
        overlay = {
            "compliance_constraints": raw_answers.get("compliance"),
            "required_tools": raw_answers.get("tools", {}).get("required", []),
            "forbidden_tools": raw_answers.get("tools", {}).get("forbidden", []),
            "output_format": self._parse_format(raw_answers.get("format")),
            "priority": raw_answers.get("priority", "balanced"),
            "failure_history": raw_answers.get("failures", []),
            "created_at": datetime.now().isoformat(),
        }

        logger.info("Local overlay structured")
        return overlay

    def _parse_format(self, format_string: Optional[str]) -> Optional[Dict]:
        """Parse output format specification into structured format."""
        if not format_string:
            return None

        # Simple parsing - in production would be more sophisticated
        format_dict = {
            "description": format_string,
            "example": "[Will be provided by external canon]"
        }

        return format_dict

    def _print_interview_summary(self, raw_answers: Dict) -> None:
        """Print interview summary."""
        print("\n" + "="*60)
        print("INTERVIEW SUMMARY")
        print("="*60 + "\n")

        if raw_answers.get("compliance"):
            print(f"Compliance: {raw_answers['compliance']}\n")

        if raw_answers.get("tools"):
            tools = raw_answers["tools"]
            if tools.get("required"):
                print(f"Required tools: {', '.join(tools['required'])}")
            if tools.get("forbidden"):
                print(f"Forbidden tools: {', '.join(tools['forbidden'])}\n")

        if raw_answers.get("format"):
            print(f"Output format: {raw_answers['format']}\n")

        print(f"Priority: {raw_answers.get('priority', 'balanced')}\n")

        if raw_answers.get("failures"):
            print("Common failures:")
            for failure in raw_answers["failures"]:
                print(f"  • {failure}\n")

        print("="*60 + "\n")

    def save_to_file(self, overlay: Dict, filepath: str) -> None:
        """Save overlay to user_overrides.md."""
        md_content = f"""# User Overrides and Local Constraints

Generated: {datetime.now().isoformat()}

## Compliance Requirements

{overlay.get('compliance_constraints') or 'None specified'}

## Tool Requirements

**Must use:**
{chr(10).join(f"- {tool}" for tool in overlay.get('required_tools', [])) or "- No specific requirements"}

**Cannot use:**
{chr(10).join(f"- {tool}" for tool in overlay.get('forbidden_tools', [])) or "- No restrictions"}

## Output Format

{overlay.get('output_format', {}).get('description') or 'Not specified'}

## Priority

{overlay.get('priority', 'balanced').title()}

## Known Failure Patterns

Common issues in your context:
{chr(10).join(f"- {failure}" for failure in overlay.get('failure_history', [])) or "- None documented yet"}

## Notes

These constraints will be compiled into the SKILL.md with highest priority.
If conflicts arise between these constraints and external best practices,
these local constraints take precedence (except for tool compatibility issues).
"""

        with open(filepath, "w") as f:
            f.write(md_content)

        logger.info(f"Overlay saved to {filepath}")

    async def quick_interview(self, scope_card: Dict) -> Dict:
        """
        Quick interview - just the 5 most critical questions.

        Returns overlay dict ready for compilation.
        """
        return await self._interview_interactive(scope_card)
