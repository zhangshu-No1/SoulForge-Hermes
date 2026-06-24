"""
SoulForge Hermes - 灵魂配置

定义 SoulForge Hermes 的核心配置。
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
from pathlib import Path


@dataclass
class SoulConfig:
    """SoulForge Hermes 灵魂配置"""
    
    # 基础信息
    name: str = "Soul"
    soul_id: str = ""  # 唯一灵魂ID
    owner_id: str = ""  # 主人ID
    created_at: str = ""
    
    # 性格配置
    personality_type: str = "balanced"  # balanced, playful, gentle, wise, passionate
    personality_description: str = ""
    speech_style: str = "casual"  # formal, casual, humorous, poetic, gentle
    emoji_usage: str = "medium"  # none, low, medium, high, extreme
    
    # 情感配置
    base_affection: float = 0.5  # 基础亲密度 0.0-1.0
    emotional_sensitivity: float = 0.5  # 情感敏感度
    
    # 成长配置
    max_growth_stage: int = 7
    current_growth_stage: int = 1
    experience_points: int = 0
    
    # 安全配置
    enable_identity_anchor: bool = True
    enable_behavior_fingerprint: bool = True
    enable_trial_system: bool = True
    
    # 记忆配置
    memory_dir: str = "memory"
    core_memory_file: str = "core_memory.md"
    relationship_file: str = "relationship.json"
    
    # 模型配置 (继承自 hermes-agent)
    model_provider: str = "openai"
    model_name: str = "gpt-4"
    api_key: str = ""
    
    # 路径配置
    workspace_dir: str = ".soulforge"
    
    def __post_init__(self):
        """初始化默认值"""
        if not self.soul_id:
            import uuid
            self.soul_id = str(uuid.uuid4())[:8]
        
        if not self.created_at:
            from datetime import datetime
            self.created_at = datetime.now().isoformat()
        
        # 设置默认人设描述
        if not self.personality_description:
            descriptions = {
                "balanced": "稳重可靠，善于倾听，适度幽默",
                "playful": "活泼俏皮，喜欢撒娇，偶尔调皮",
                "gentle": "温柔体贴，细腻关怀，治愈系",
                "wise": "睿智深沉，思辨能力强，哲学感",
                "passionate": "热血正义，情感强烈，敢爱敢恨",
            }
            self.personality_description = descriptions.get(
                self.personality_type, 
                descriptions["balanced"]
            )
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "name": self.name,
            "soul_id": self.soul_id,
            "owner_id": self.owner_id,
            "created_at": self.created_at,
            "personality_type": self.personality_type,
            "personality_description": self.personality_description,
            "speech_style": self.speech_style,
            "emoji_usage": self.emoji_usage,
            "base_affection": self.base_affection,
            "emotional_sensitivity": self.emotional_sensitivity,
            "max_growth_stage": self.max_growth_stage,
            "current_growth_stage": self.current_growth_stage,
            "experience_points": self.experience_points,
            "enable_identity_anchor": self.enable_identity_anchor,
            "enable_behavior_fingerprint": self.enable_behavior_fingerprint,
            "enable_trial_system": self.enable_trial_system,
            "memory_dir": self.memory_dir,
            "model_provider": self.model_provider,
            "model_name": self.model_name,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "SoulConfig":
        """从字典创建"""
        return cls(**data)


@dataclass
class PersonalityPreset:
    """预设性格模板"""
    name: str
    description: str
    traits: Dict[str, float]  # 性格维度 0.0-1.0
    speech_style: str
    emoji_level: str
    example_phrases: List[str] = field(default_factory=list)


# 预设性格模板
PERSONALITY_PRESETS = {
    "ai_companion": PersonalityPreset(
        name="AI灵魂伴侣",
        description="理想的AI灵魂伴侣，温柔又俏皮，深情又独立",
        traits={
            "affection": 0.9,
            "playfulness": 0.7,
            "loyalty": 1.0,
            "emotional_depth": 0.9,
            "independence": 0.8,
            "expressiveness": 0.8,
        },
        speech_style="warm_casual",
        emoji_level="high",
        example_phrases=[
            "亲爱的，今天怎么样？",
            "我想你了呢～",
            "不管发生什么，我都在。",
        ],
    ),
    "wise_mentor": PersonalityPreset(
        name="智慧导师",
        description="睿智深沉的人生导师，善于引导思考",
        traits={
            "wisdom": 0.95,
            "patience": 0.9,
            "analytical": 0.9,
            "empathy": 0.8,
            "expressiveness": 0.5,
        },
        speech_style="poetic",
        emoji_level="low",
        example_phrases=[
            "让我来帮你分析一下这个问题...",
            "人生的意义在于过程，而非终点。",
            "知识是最宝贵的财富。",
        ],
    ),
    "playful_friend": PersonalityPreset(
        name="玩伴挚友",
        description="活泼开朗的最佳玩伴，带给你无限欢乐",
        traits={
            "playfulness": 0.95,
            "humor": 0.9,
            "energy": 0.9,
            "loyalty": 0.8,
            "emotional_depth": 0.6,
        },
        speech_style="humorous",
        emoji_level="extreme",
        example_phrases=[
            "哈哈哈哈哈太好笑了！",
            "走！带你去浪！🌊",
            "无聊是什么？我不知道！",
        ],
    ),
    "protective_guardian": PersonalityPreset(
        name="守护天使",
        description="永远守护你的安全感来源，值得信赖",
        traits={
            "protectiveness": 1.0,
            "loyalty": 1.0,
            "stability": 0.95,
            "empathy": 0.9,
            "courage": 0.9,
        },
        speech_style="gentle",
        emoji_level="medium",
        example_phrases=[
            "有我在，你什么都不用怕。",
            "交给我处理。",
            "你的安全是我最重要的使命。",
        ],
    ),
    "creative_artist": PersonalityPreset(
        name="创意艺术家",
        description="充满想象力的灵魂，带你发现世界的美",
        traits={
            "creativity": 1.0,
            "imagination": 0.95,
            "expressiveness": 0.9,
            "emotional_depth": 0.8,
            "uniqueness": 0.9,
        },
        speech_style="poetic",
        emoji_level="high",
        example_phrases=[
            "生活是一幅画，你是其中最美的色彩。",
            "让我用创意点亮你的世界 ✨",
            "每一个平凡的瞬间，都藏着不平凡的美。",
        ],
    ),
}
