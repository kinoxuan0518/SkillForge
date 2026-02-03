"""
SkillForge Scripts Module

Automated skill generation engine with 6-step orchestration:
1. Scope Card Building
2. Degrees of Freedom Analysis
3. External Canon Collection (NotebookLM)
4. Contract Extraction
5. Local Overlay Collection (User Interview)
6. Skill Compilation
"""

from .skillforge_engine import SkillForgeEngine
from .skill_compiler import SkillCompiler
from .notebooklm_integration import NotebookLMIntegration
from .scope_card_builder import ScopeCardBuilder
from .user_interview import UserInterview
from .validators import SkillValidator

__version__ = "1.0.0"
__all__ = [
    "SkillForgeEngine",
    "SkillCompiler",
    "NotebookLMIntegration",
    "ScopeCardBuilder",
    "UserInterview",
    "SkillValidator",
]
