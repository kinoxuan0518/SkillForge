"""
SkillForge Engine - Main orchestration for automated skill generation.

Automates the 6-step SkillForge process:
1. Scope Card Generation (Step 1)
2. Decision on Degrees of Freedom (Step 2)
3. External Canon Collection via NotebookLM (Step 3)
4. Contract Extraction (Step 4)
5. Local Overlay via User Interview (Step 5)
6. Skill Compilation (Step 6)
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ScopeCard:
    """Step 1 output: Skill scope definition."""
    goal: str  # One-sentence goal
    trigger_words: List[str]  # 5+ trigger phrases
    must_cover: List[str]  # 3+ items
    must_not_cover: List[str]  # 3+ items
    output_form: str  # template/script/decision-tree/etc
    success_criteria: List[str]  # Measurable success criteria
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

    def validate(self) -> tuple[bool, List[str]]:
        """Validate scope card completeness."""
        errors = []

        if not self.goal or len(self.goal.strip()) < 10:
            errors.append("Goal must be at least 10 characters")

        if len(self.trigger_words) < 5:
            errors.append(f"Need 5+ trigger words, got {len(self.trigger_words)}")

        if len(self.must_cover) < 3:
            errors.append(f"Need 3+ must_cover items, got {len(self.must_cover)}")

        if len(self.must_not_cover) < 3:
            errors.append(f"Need 3+ must_not_cover items, got {len(self.must_not_cover)}")

        if not self.output_form:
            errors.append("Output form must be specified")

        if len(self.success_criteria) < 1:
            errors.append("Need at least 1 success criterion")

        return len(errors) == 0, errors


@dataclass
class ExternalCanon:
    """Step 3 output: External knowledge from NotebookLM."""
    notebook_id: str  # NotebookLM notebook ID
    sources: List[Dict[str, str]]  # [{title, url, relevance}]
    quickstart: str  # 3-step quickstart
    decision_points: List[str]  # if/else decision points
    templates: List[Dict[str, str]]  # [{name, content}]
    failure_modes: List[Dict[str, str]]  # [{symptom, fix}]
    edge_cases: List[str]  # Edge case descriptions
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


@dataclass
class LocalOverlay:
    """Step 5 output: User/organization constraints."""
    compliance_constraints: str  # Red lines
    required_tools: List[str]  # Must use
    forbidden_tools: List[str]  # Cannot use
    output_format: Optional[Dict] = None  # Fixed format requirements
    priority: str = None  # speed/accuracy/explainability/consistency
    failure_history: List[str] = None  # Common failure patterns
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.failure_history is None:
            self.failure_history = []


class SkillForgeEngine:
    """
    Main orchestration engine for the 6-step SkillForge process.
    """

    def __init__(self, storage_dir: str = None):
        """
        Initialize the engine.

        Args:
            storage_dir: Directory for storing generated artifacts
        """
        self.storage_dir = Path(storage_dir) if storage_dir else Path.cwd() / "skillforge_output"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Sub-engines (lazy loaded)
        self._scope_builder = None
        self._notebooklm_integration = None
        self._interviewer = None
        self._compiler = None
        self._validator = None

    @property
    def scope_builder(self):
        """Lazy load scope card builder."""
        if self._scope_builder is None:
            from scope_card_builder import ScopeCardBuilder
            self._scope_builder = ScopeCardBuilder()
        return self._scope_builder

    @property
    def notebooklm_integration(self):
        """Lazy load NotebookLM integration."""
        if self._notebooklm_integration is None:
            from notebooklm_integration import NotebookLMIntegration
            self._notebooklm_integration = NotebookLMIntegration()
        return self._notebooklm_integration

    @property
    def interviewer(self):
        """Lazy load user interviewer."""
        if self._interviewer is None:
            from user_interview import UserInterview
            self._interviewer = UserInterview()
        return self._interviewer

    @property
    def compiler(self):
        """Lazy load skill compiler."""
        if self._compiler is None:
            from skill_compiler import SkillCompiler
            self._compiler = SkillCompiler()
        return self._compiler

    @property
    def validator(self):
        """Lazy load validator."""
        if self._validator is None:
            from validators import SkillValidator
            self._validator = SkillValidator()
        return self._validator

    async def generate_skill(self, user_request: str, interactive: bool = True) -> Dict:
        """
        Generate a new skill from a user request.

        This is the main entry point that orchestrates all 6 steps:
        1. Build scope card
        2. Determine degrees of freedom
        3. Collect external canon via NotebookLM
        4. Extract contract
        5. Collect local overlay via user interview
        6. Compile SKILL.md

        Args:
            user_request: User's skill request (e.g., "make a skill for X")
            interactive: Whether to prompt user for input

        Returns:
            Dict with generated skill structure and metadata
        """
        logger.info(f"Starting skill generation for: {user_request}")

        result = {
            "status": "generating",
            "steps": {},
            "artifacts": [],
            "errors": [],
            "warnings": []
        }

        try:
            # Step 1: Scope Card
            logger.info("Step 1: Building scope card...")
            scope_card = await self._step1_scope_card(user_request, interactive)
            result["steps"]["scope_card"] = asdict(scope_card)

            # Step 2: Degrees of Freedom
            logger.info("Step 2: Determining degrees of freedom...")
            degrees_of_freedom = self._step2_degrees_of_freedom(scope_card)
            result["steps"]["degrees_of_freedom"] = degrees_of_freedom

            # Step 3: External Canon
            logger.info("Step 3: Collecting external canon from NotebookLM...")
            canon = await self._step3_external_canon(scope_card)
            result["steps"]["external_canon"] = asdict(canon)

            # Step 4: Contract Extraction
            logger.info("Step 4: Extracting contract...")
            contract = self._step4_contract_extraction(canon)
            result["steps"]["contract"] = contract

            # Step 5: Local Overlay
            logger.info("Step 5: Collecting user constraints...")
            overlay = await self._step5_local_overlay(scope_card, interactive)
            result["steps"]["local_overlay"] = asdict(overlay)

            # Step 6: Skill Compilation
            logger.info("Step 6: Compiling SKILL.md...")
            skill_md = self._step6_compilation(scope_card, canon, overlay)
            result["steps"]["skill_md"] = skill_md

            # Quality Gates
            logger.info("Validating quality gates...")
            validation = self.validator.validate_skill(skill_md, scope_card, canon)
            result["validation"] = validation

            if not validation["passed"]:
                result["status"] = "failed_validation"
                result["errors"].extend(validation["errors"])
            else:
                result["status"] = "success"

            # Save artifacts
            await self._save_artifacts(result)
            logger.info(f"Skill generation completed: {result['status']}")

        except Exception as e:
            logger.error(f"Error during skill generation: {e}", exc_info=True)
            result["status"] = "error"
            result["errors"].append(str(e))

        return result

    async def _step1_scope_card(self, user_request: str, interactive: bool) -> ScopeCard:
        """Step 1: Generate scope card."""
        return await self.scope_builder.build(user_request, interactive=interactive)

    def _step2_degrees_of_freedom(self, scope_card: ScopeCard) -> Dict:
        """Step 2: Determine degrees of freedom based on scope card."""
        # Analyze scope card complexity
        total_items = len(scope_card.must_cover) + len(scope_card.must_not_cover)

        if total_items <= 6 and len(scope_card.trigger_words) <= 5:
            freedom = "low"
            rationale = "Simple, well-defined scope → Use scripts with fixed steps"
        elif total_items <= 12:
            freedom = "medium"
            rationale = "Moderate complexity → Use parametric scripts + references"
        else:
            freedom = "high"
            rationale = "Complex, context-dependent → Use SKILL.md framework + examples"

        return {
            "freedom_level": freedom,
            "rationale": rationale,
            "suggested_resources": self._suggest_resources(freedom, scope_card)
        }

    def _suggest_resources(self, freedom: str, scope_card: ScopeCard) -> Dict:
        """Suggest which resources to use based on freedom level."""
        return {
            "skill_md_guidance": self._get_skill_md_guidance(freedom),
            "script_count": 1 if freedom == "low" else 0,
            "reference_docs": self._get_reference_docs(scope_card)
        }

    def _get_skill_md_guidance(self, freedom: str) -> str:
        if freedom == "low":
            return "Minimal: Just Quickstart + Guardrails + Failure modes"
        elif freedom == "medium":
            return "Standard: Quickstart + Workflow + Guardrails + Templates + Failure modes"
        else:
            return "Comprehensive: All sections + complex decision trees + extensive examples"

    def _get_reference_docs(self, scope_card: ScopeCard) -> List[str]:
        """Determine which reference docs are needed."""
        docs = []
        if "template" in scope_card.output_form.lower():
            docs.append("templates.md")
        if len(scope_card.must_not_cover) > 0:
            docs.append("edge_cases.md")
        docs.append("failure_modes.md")
        return docs

    async def _step3_external_canon(self, scope_card: ScopeCard) -> ExternalCanon:
        """Step 3: Collect external canon from NotebookLM."""
        return await self.notebooklm_integration.collect_canon(scope_card)

    def _step4_contract_extraction(self, canon: ExternalCanon) -> Dict:
        """Step 4: Extract executable contract from canon."""
        return {
            "quickstart": canon.quickstart,
            "decision_points": canon.decision_points,
            "templates": canon.templates,
            "failure_modes": canon.failure_modes,
            "edge_cases": canon.edge_cases
        }

    async def _step5_local_overlay(self, scope_card: ScopeCard, interactive: bool) -> LocalOverlay:
        """Step 5: Collect local overlay (user constraints)."""
        return await self.interviewer.interview(scope_card, interactive=interactive)

    def _step6_compilation(self, scope_card: ScopeCard, canon: ExternalCanon, overlay: LocalOverlay) -> str:
        """Step 6: Compile external canon + local overlay into SKILL.md."""
        return self.compiler.compile(scope_card, canon, overlay)

    async def _save_artifacts(self, result: Dict) -> None:
        """Save all artifacts to disk."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = self.storage_dir / f"skill_{timestamp}"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save JSON metadata
        with open(output_dir / "metadata.json", "w") as f:
            json.dump(result, f, indent=2)

        # Save SKILL.md
        if "skill_md" in result.get("steps", {}):
            with open(output_dir / "SKILL.md", "w") as f:
                f.write(result["steps"]["skill_md"])

        logger.info(f"Artifacts saved to {output_dir}")
        result["artifacts"].append(str(output_dir))


# CLI Entry Point
async def main():
    """CLI entry point for SkillForge engine."""
    import sys
    import asyncio

    if len(sys.argv) < 2:
        print("Usage: python skillforge_engine.py <user_request>")
        print("Example: python skillforge_engine.py 'make a skill for Python linting'")
        sys.exit(1)

    user_request = " ".join(sys.argv[1:])
    engine = SkillForgeEngine()

    result = await engine.generate_skill(user_request, interactive=True)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
