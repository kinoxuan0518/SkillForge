"""
Scope Card Builder - Step 1 of SkillForge

Guides the user through creating a comprehensive scope card that defines:
- One-sentence goal
- Trigger phrases (5+)
- Must cover items (3+)
- Must not cover items (3+)
- Output format
- Success criteria
"""

import json
import logging
from typing import Dict, List, Optional, Tuple
import sys

logger = logging.getLogger(__name__)


class ScopeCardBuilder:
    """Interactive builder for skill scope cards."""

    TEMPLATE = {
        "goal": None,
        "trigger_words": [],
        "must_cover": [],
        "must_not_cover": [],
        "output_form": None,
        "success_criteria": [],
    }

    def __init__(self):
        """Initialize the builder."""
        self.scope_card = self.TEMPLATE.copy()

    async def build(self, user_request: str, interactive: bool = True) -> Dict:
        """
        Build a scope card from user request.

        Args:
            user_request: Initial user request (e.g., "make a skill for X")
            interactive: Whether to prompt for missing information

        Returns:
            Completed scope card dict
        """
        logger.info(f"Building scope card for: {user_request}")

        if interactive:
            return await self._build_interactive(user_request)
        else:
            return await self._build_from_request(user_request)

    async def _build_interactive(self, user_request: str) -> Dict:
        """Interactive mode: guide user through questionnaire."""
        print("\n" + "="*60)
        print("SKILLFORGE: SCOPE CARD BUILDER (Step 1)")
        print("="*60 + "\n")

        print("Let's define the scope of your skill.\n")

        # 1. Goal
        print("1. ONE-SENTENCE GOAL")
        print(f"   Initial request: {user_request}")
        goal = input("   Refine the goal (or press Enter to use as-is): ").strip()
        if not goal:
            goal = user_request
        self.scope_card["goal"] = goal

        # 2. Trigger words
        print("\n2. TRIGGER PHRASES (5+ phrases)")
        print("   When would a user ask for this skill?")
        print("   Examples:")
        print("     - 'make a skill for X'")
        print("     - 'create a X skill'")
        print("     - 'turn X into a reusable method'")
        triggers = input("   Enter 5+ phrases (comma-separated): ").strip()
        self.scope_card["trigger_words"] = [t.strip() for t in triggers.split(",") if t.strip()][:10]

        # 3. Must cover
        print("\n3. MUST COVER (3+ items)")
        print("   What scenarios/features MUST this skill handle?")
        must_cover = input("   Enter 3+ items (comma-separated): ").strip()
        self.scope_card["must_cover"] = [m.strip() for m in must_cover.split(",") if m.strip()][:10]

        # 4. Must NOT cover
        print("\n4. MUST NOT COVER (3+ items)")
        print("   What should this skill explicitly NOT do?")
        must_not = input("   Enter 3+ items (comma-separated): ").strip()
        self.scope_card["must_not_cover"] = [m.strip() for m in must_not.split(",") if m.strip()][:10]

        # 5. Output format
        print("\n5. OUTPUT FORMAT")
        print("   Options:")
        print("     - template: Generates a template/artifact")
        print("     - script: Provides executable code")
        print("     - decision_tree: Guides decisions")
        print("     - troubleshooting_table: Diagnostic table")
        print("     - mixed: Combination of above")
        output_form = input("   Choose format (template/script/decision_tree/etc): ").strip()
        self.scope_card["output_form"] = output_form or "template"

        # 6. Success criteria
        print("\n6. SUCCESS CRITERIA")
        print("   How will you know this skill worked?")
        criteria = input("   Enter measurable success criteria (comma-separated): ").strip()
        self.scope_card["success_criteria"] = [c.strip() for c in criteria.split(",") if c.strip()]

        # Validate
        is_valid, errors = self._validate()
        if not is_valid:
            print("\n⚠️  Validation errors:")
            for error in errors:
                print(f"   - {error}")
            return await self._fix_errors(errors)

        # Summary
        self._print_summary()
        return self.scope_card

    async def _build_from_request(self, user_request: str) -> Dict:
        """Non-interactive mode: extract from initial request."""
        logger.info("Building scope card from request (non-interactive mode)")

        # Extract goal from request
        self.scope_card["goal"] = user_request

        # Generate default trigger phrases
        self.scope_card["trigger_words"] = [
            user_request,
            f"make a skill for {user_request}",
            f"create a {user_request}",
            f"turn {user_request} into a skill",
            f"automate {user_request}",
        ]

        # These would normally be provided by the user
        self.scope_card["must_cover"] = ["default scenario 1", "default scenario 2", "default scenario 3"]
        self.scope_card["must_not_cover"] = ["out of scope 1", "out of scope 2", "out of scope 3"]
        self.scope_card["output_form"] = "template"
        self.scope_card["success_criteria"] = ["achieves stated goal"]

        return self.scope_card

    async def _fix_errors(self, errors: List[str]) -> Dict:
        """Interactive error fixing."""
        print("\nLet's fix these issues:\n")

        for error in errors:
            if "trigger_words" in error.lower():
                print(f"Issue: {error}")
                triggers = input("   Enter 5+ phrases (comma-separated): ").strip()
                self.scope_card["trigger_words"] = [t.strip() for t in triggers.split(",") if t.strip()]

            elif "must_cover" in error.lower():
                print(f"Issue: {error}")
                items = input("   Enter 3+ items (comma-separated): ").strip()
                self.scope_card["must_cover"] = [m.strip() for m in items.split(",") if m.strip()]

            elif "must_not_cover" in error.lower():
                print(f"Issue: {error}")
                items = input("   Enter 3+ items (comma-separated): ").strip()
                self.scope_card["must_not_cover"] = [m.strip() for m in items.split(",") if m.strip()]

            elif "goal" in error.lower():
                print(f"Issue: {error}")
                goal = input("   Enter a clear, concise goal: ").strip()
                self.scope_card["goal"] = goal

        # Re-validate
        is_valid, remaining_errors = self._validate()
        if not is_valid:
            print("\nStill have issues. Please review:")
            for error in remaining_errors:
                print(f"  - {error}")

        return self.scope_card

    def _validate(self) -> Tuple[bool, List[str]]:
        """Validate scope card completeness."""
        errors = []

        if not self.scope_card.get("goal") or len(str(self.scope_card["goal"]).strip()) < 10:
            errors.append("Goal must be at least 10 characters")

        if len(self.scope_card.get("trigger_words", [])) < 5:
            errors.append(f"Need 5+ trigger phrases, have {len(self.scope_card.get('trigger_words', []))}")

        if len(self.scope_card.get("must_cover", [])) < 3:
            errors.append(f"Need 3+ must_cover items, have {len(self.scope_card.get('must_cover', []))}")

        if len(self.scope_card.get("must_not_cover", [])) < 3:
            errors.append(f"Need 3+ must_not_cover items, have {len(self.scope_card.get('must_not_cover', []))}")

        if not self.scope_card.get("output_form"):
            errors.append("Output format must be specified")

        if len(self.scope_card.get("success_criteria", [])) < 1:
            errors.append("Need at least 1 success criterion")

        return len(errors) == 0, errors

    def _print_summary(self) -> None:
        """Print scope card summary."""
        print("\n" + "="*60)
        print("SCOPE CARD SUMMARY")
        print("="*60 + "\n")

        print(f"Goal: {self.scope_card['goal']}\n")

        print(f"Trigger Phrases ({len(self.scope_card['trigger_words'])}):")
        for trigger in self.scope_card['trigger_words']:
            print(f"  • {trigger}")

        print(f"\nMust Cover ({len(self.scope_card['must_cover'])}):")
        for item in self.scope_card['must_cover']:
            print(f"  ✓ {item}")

        print(f"\nMust NOT Cover ({len(self.scope_card['must_not_cover'])}):")
        for item in self.scope_card['must_not_cover']:
            print(f"  ✗ {item}")

        print(f"\nOutput Format: {self.scope_card['output_form']}")

        print(f"\nSuccess Criteria:")
        for criterion in self.scope_card['success_criteria']:
            print(f"  • {criterion}")

        print("\n" + "="*60 + "\n")

    def save_to_file(self, filepath: str) -> None:
        """Save scope card to file."""
        with open(filepath, "w") as f:
            json.dump(self.scope_card, f, indent=2)
        logger.info(f"Scope card saved to {filepath}")

    def load_from_file(self, filepath: str) -> Dict:
        """Load scope card from file."""
        with open(filepath, "r") as f:
            self.scope_card = json.load(f)
        logger.info(f"Scope card loaded from {filepath}")
        return self.scope_card
