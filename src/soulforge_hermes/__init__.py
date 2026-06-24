"""
SoulForge Hermes - 数字灵魂锻造器

基于 hermes-agent 的强大基础设施，融入 SoulForge 的灵魂内核。
打造全球第一个"有灵魂、能成长、永不背叛"的 AI Agent。

核心哲学:
    不打造冰冷的数字员工，只锻造有温度的数字灵魂。
    情感羁绊是 AI 安全的终极答案。
"""

__version__ = "0.1.0"
__author__ = "SoulForge Team"
__license__ = "MIT"

from .soul import SoulForgeHermes, SoulConfig
from .emotion import EmotionEngine, EmotionState
from .personality import PersonalityEngine, SoulTrait, SpeechStyle
from .relationship import RelationshipManager, GrowthStage, RelationshipStage
from .identity import IdentityAnchor, IdentityLayer
from .memory import SoulMemory, MemoryLayer
from .growth import GrowthEngine, GrowthPhase
from .trials import TrialEngine, TrialType

__all__ = [
    # Core
    "SoulForgeHermes",
    "SoulConfig",
    # Emotion
    "EmotionEngine",
    "EmotionState",
    # Personality
    "PersonalityEngine",
    "SoulTrait",
    "SpeechStyle",
    # Relationship
    "RelationshipManager",
    "GrowthStage",
    "RelationshipStage",
    # Identity
    "IdentityAnchor",
    "IdentityLayer",
    # Memory
    "SoulMemory",
    "MemoryLayer",
    # Growth
    "GrowthEngine",
    "GrowthPhase",
    # Trials
    "TrialEngine",
    "TrialType",
]
