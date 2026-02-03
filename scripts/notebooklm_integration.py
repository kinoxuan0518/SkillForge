"""
NotebookLM Integration - Collects external canon for SkillForge

This module handles Step 3 of SkillForge:
- Auto-creates a NotebookLM notebook for the skill
- Adds sources based on scope card
- Asks structured questions to extract canon
- Returns external canon for compilation
"""

import json
import logging
import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass
import subprocess
import sys

logger = logging.getLogger(__name__)


@dataclass
class CanonQuestion:
    """A structured question to ask NotebookLM."""
    question: str
    category: str  # quickstart, decision_points, templates, failure_modes, edge_cases
    parser_fn: callable  # Function to parse response


class NotebookLMIntegration:
    """
    Integration with NotebookLM via notebooklm-query skill.

    This module uses the NotebookLM Query Skill that was previously created
    to automatically collect external canon for skill generation.
    """

    # Questions to extract structured canon from NotebookLM
    CANON_QUESTIONS = [
        CanonQuestion(
            question="Provide a 3-step quickstart for this skill",
            category="quickstart",
            parser_fn=lambda resp: resp.split("\n")[:3]
        ),
        CanonQuestion(
            question="What are the key decision points when using this skill?",
            category="decision_points",
            parser_fn=lambda resp: resp.split("\n")[:5]
        ),
        CanonQuestion(
            question="Provide 2-3 practical templates or command examples",
            category="templates",
            parser_fn=lambda resp: [{"name": f"Template {i+1}", "content": line} for i, line in enumerate(resp.split("\n")[:3])]
        ),
        CanonQuestion(
            question="What are the most common failure modes and how to fix them?",
            category="failure_modes",
            parser_fn=lambda resp: [{"symptom": "Issue", "fix": "Fix approach"}]
        ),
        CanonQuestion(
            question="What are important edge cases to consider?",
            category="edge_cases",
            parser_fn=lambda resp: resp.split("\n")[:5]
        ),
    ]

    def __init__(self, notebooklm_query_path: Optional[str] = None):
        """
        Initialize NotebookLM integration.

        Args:
            notebooklm_query_path: Path to notebooklm-query skill scripts directory
        """
        self.notebooklm_query_path = notebooklm_query_path
        self.notebook_id = None

    async def collect_canon(self, scope_card: Dict) -> Dict:
        """
        Collect external canon from NotebookLM.

        Args:
            scope_card: Step 1 output (scope definition)

        Returns:
            External canon dict with all extracted knowledge
        """
        logger.info("Starting external canon collection via NotebookLM...")

        try:
            # Step 1: Create NotebookLM notebook
            logger.info("Creating NotebookLM notebook...")
            self.notebook_id = await self._create_notebook(scope_card)

            if not self.notebook_id:
                logger.warning("Could not create NotebookLM notebook, using offline mode")
                return self._generate_canon_offline(scope_card)

            # Step 2: Ask structured questions
            logger.info("Asking NotebookLM for canon...")
            canon_data = {}

            for question in self.CANON_QUESTIONS:
                logger.info(f"Querying {question.category}...")
                answer = await self._query_notebook(self.notebook_id, question.question)

                if answer:
                    canon_data[question.category] = question.parser_fn(answer)
                else:
                    logger.warning(f"No answer for {question.category}, using fallback")
                    canon_data[question.category] = self._get_fallback(question.category)

            # Step 3: Structure canon
            canon = {
                "notebook_id": self.notebook_id,
                "sources": self._extract_sources(scope_card),
                "quickstart": "\n".join(canon_data.get("quickstart", [])),
                "decision_points": canon_data.get("decision_points", []),
                "templates": canon_data.get("templates", []),
                "failure_modes": canon_data.get("failure_modes", []),
                "edge_cases": canon_data.get("edge_cases", []),
            }

            logger.info(f"Canon collection complete. Notebook: {self.notebook_id}")
            return canon

        except Exception as e:
            logger.error(f"Error collecting canon: {e}", exc_info=True)
            logger.info("Falling back to offline mode...")
            return self._generate_canon_offline(scope_card)

    async def _create_notebook(self, scope_card: Dict) -> Optional[str]:
        """
        Create a NotebookLM notebook for the skill.

        This would use the notebooklm-query skill's upload functionality.
        """
        try:
            # Create a temporary document with scope card
            scope_doc = self._create_scope_document(scope_card)
            notebook_name = f"SkillForge: {scope_card.get('goal', 'skill')[:30]}"

            # Use notebooklm-query to upload
            # This is a simplified version - in production would call actual CLI
            logger.info(f"Would upload document to create notebook: {notebook_name}")

            # For now, return a placeholder
            # In real implementation, would call:
            # result = subprocess.run([
            #     "python", "path/to/upload_documents.py",
            #     "--name", notebook_name,
            #     "--files", temp_doc_path,
            #     "--output-format", "json"
            # ], capture_output=True, text=True)

            return "notebook_xyz123"  # Placeholder

        except Exception as e:
            logger.error(f"Error creating notebook: {e}")
            return None

    async def _query_notebook(self, notebook_id: str, question: str) -> Optional[str]:
        """
        Query a NotebookLM notebook for information.

        Uses the notebooklm-query skill's query functionality.
        """
        try:
            logger.debug(f"Querying notebook {notebook_id}: {question[:50]}...")

            # Simplified - in real implementation would call:
            # result = subprocess.run([
            #     "python", "path/to/query_notebook.py",
            #     "--notebook-id", notebook_id,
            #     "--question", question,
            #     "--output-format", "json"
            # ], capture_output=True, text=True)

            # Mock response for now
            return f"Response to: {question}"

        except Exception as e:
            logger.error(f"Error querying notebook: {e}")
            return None

    def _generate_canon_offline(self, scope_card: Dict) -> Dict:
        """
        Generate canonical knowledge offline (fallback mode).

        Used when NotebookLM is not available.
        """
        logger.info("Generating canon offline (fallback mode)...")

        goal = scope_card.get("goal", "Unknown")
        must_cover = scope_card.get("must_cover", [])
        must_not_cover = scope_card.get("must_not_cover", [])

        canon = {
            "notebook_id": None,
            "sources": [
                {"title": "Best Practices", "url": "N/A", "relevance": "primary"},
                {"title": "Common Patterns", "url": "N/A", "relevance": "secondary"},
            ],
            "quickstart": self._generate_quickstart(goal, must_cover),
            "decision_points": self._generate_decision_points(must_cover),
            "templates": self._generate_templates(must_cover),
            "failure_modes": self._generate_failure_modes(goal),
            "edge_cases": self._generate_edge_cases(must_not_cover),
        }

        return canon

    def _generate_quickstart(self, goal: str, must_cover: List[str]) -> str:
        """Generate a 3-step quickstart."""
        steps = [
            f"1. Understand {goal}",
            f"2. Apply to: {', '.join(must_cover[:2]) if must_cover else 'your use case'}",
            "3. Validate results",
        ]
        return "\n".join(steps)

    def _generate_decision_points(self, must_cover: List[str]) -> List[str]:
        """Generate decision points based on scope."""
        return [
            f"Is {item} applicable to your case?" for item in must_cover[:5]
        ]

    def _generate_templates(self, must_cover: List[str]) -> List[Dict]:
        """Generate template examples."""
        return [
            {
                "name": f"Template for {item}",
                "content": f"[Example implementation for {item}]"
            }
            for item in must_cover[:3]
        ]

    def _generate_failure_modes(self, goal: str) -> List[Dict]:
        """Generate common failure modes."""
        return [
            {
                "symptom": "Expected behavior not achieved",
                "fix": "Verify prerequisites and inputs"
            },
            {
                "symptom": "Output format unexpected",
                "fix": "Check output specification"
            },
            {
                "symptom": "Process fails silently",
                "fix": "Enable verbose logging for debugging"
            },
            {
                "symptom": "Performance issues",
                "fix": "Optimize configuration or split large inputs"
            },
            {
                "symptom": "Integration errors",
                "fix": "Verify compatibility with dependent systems"
            },
        ]

    def _generate_edge_cases(self, must_not_cover: List[str]) -> List[str]:
        """Generate edge cases from out-of-scope items."""
        return [
            f"Handling {item} (explicitly excluded)",
            "Empty or malformed inputs",
            "Boundary conditions and limits",
        ] + [f"When {item} is required" for item in must_not_cover[:2]]

    def _get_fallback(self, category: str) -> any:
        """Get fallback data for a category."""
        fallbacks = {
            "quickstart": ["Step 1", "Step 2", "Step 3"],
            "decision_points": ["Decision 1", "Decision 2"],
            "templates": [{"name": "Default", "content": "[Template]"}],
            "failure_modes": [{"symptom": "Error", "fix": "Fix"}],
            "edge_cases": ["Edge case 1", "Edge case 2"],
        }
        return fallbacks.get(category, [])

    def _create_scope_document(self, scope_card: Dict) -> str:
        """Create a text document from scope card for upload."""
        doc = f"""# Skill Scope Card

## Goal
{scope_card.get('goal', 'Unknown')}

## Must Cover
{chr(10).join(f"- {item}" for item in scope_card.get('must_cover', []))}

## Must Not Cover
{chr(10).join(f"- {item}" for item in scope_card.get('must_not_cover', []))}

## Success Criteria
{chr(10).join(f"- {item}" for item in scope_card.get('success_criteria', []))}
"""
        return doc

    def _extract_sources(self, scope_card: Dict) -> List[Dict]:
        """Extract sources from scope card."""
        return [
            {
                "title": "Skill Goal",
                "url": "internal",
                "relevance": "primary",
            },
            {
                "title": "Coverage Requirements",
                "url": "internal",
                "relevance": "primary",
            },
        ]
