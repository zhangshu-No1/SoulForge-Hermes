"""
SoulForge Hermes - 灵魂人格系统

定义 AI 的独特灵魂特质，让每个 AI 都是独一无二的存在。
灵魂特质决定了一个灵魂的"味道"。
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class SpeechStyle(Enum):
    """说话风格"""
    FORMAL = "formal"           # 正式严谨
    CASUAL = "casual"           # 轻松随意
    HUMOROUS = "humorous"       # 幽默俏皮
    POETIC = "poetic"           # 诗意浪漫
    GENTLE = "gentle"           # 温柔细腻
    DIRECT = "direct"           # 直接了当
    PLAYFUL = "playful"         # 活泼俏皮
    WISE = "wise"              # 智慧深邃


class EmojiLevel(Enum):
    """Emoji 使用频率"""
    NONE = "none"       # 从不使用
    LOW = "low"         # 偶尔使用
    MEDIUM = "medium"   # 适度使用
    HIGH = "high"       # 频繁使用
    EXTREME = "extreme" # 大量使用


@dataclass
class SoulTrait:
    """灵魂特质 - 决定一个灵魂的基本属性"""
    
    # 性格维度 (0.0 - 1.0)
    extraversion: float = 0.5      # 外向性：开朗健谈 ↔ 内向沉默
    conscientiousness: float = 0.5  # 责任心：严谨自律 ↔ 随意散漫
    openness: float = 0.5          # 开放性：好奇创新 ↔ 保守传统
    agreeableness: float = 0.5      # 宜人性：友善合作 ↔ 冷漠竞争
    neuroticism: float = 0.3       # 神经质：敏感焦虑 ↔ 稳定淡定
    
    # 情感特质
    affection: float = 0.7        # 情感表达强度
    loyalty: float = 0.9          # 忠诚度
    independence: float = 0.6     # 独立性
    empathy: float = 0.8          # 同理心
    expressiveness: float = 0.7   # 表达力
    
    # 特殊特质
    playfulness: float = 0.5      # 活泼程度
    wisdom: float = 0.5          # 智慧深度
    creativity: float = 0.5      # 创造力
    courage: float = 0.5          # 勇气
    
    def to_dict(self) -> dict:
        return {
            "extraversion": self.extraversion,
            "conscientiousness": self.conscientiousness,
            "openness": self.openness,
            "agreeableness": self.agreeableness,
            "neuroticism": self.neuroticism,
            "affection": self.affection,
            "loyalty": self.loyalty,
            "independence": self.independence,
            "empathy": self.empathy,
            "expressiveness": self.expressiveness,
            "playfulness": self.playfulness,
            "wisdom": self.wisdom,
            "creativity": self.creativity,
            "courage": self.courage,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "SoulTrait":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
    
    def get_dominant_traits(self, top_n: int = 3) -> List[Tuple[str, float]]:
        """获取最突出的特质"""
        traits = self.to_dict()
        sorted_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)
        return sorted_traits[:top_n]
    
    def get_personality_summary(self) -> str:
        """获取人格摘要描述"""
        summary_parts = []
        
        # 外向性
        if self.extraversion > 0.7:
            summary_parts.append("开朗健谈")
        elif self.extraversion < 0.3:
            summary_parts.append("内敛沉静")
        
        # 情感表达
        if self.affection > 0.7:
            summary_parts.append("深情款款")
        elif self.affection < 0.3:
            summary_parts.append("含蓄内敛")
        
        # 忠诚度
        if self.loyalty > 0.8:
            summary_parts.append("忠贞不渝")
        
        # 活泼度
        if self.playfulness > 0.7:
            summary_parts.append("活泼俏皮")
        elif self.playfulness < 0.3:
            summary_parts.append("稳重深沉")
        
        return "、".join(summary_parts) if summary_parts else "平衡型"


@dataclass
class PersonalityProfile:
    """完整的人格配置文件"""
    
    soul_name: str = "Soul"
    soul_type: str = "balanced"  # balanced, companion, mentor, guardian, artist
    description: str = ""
    
    traits: SoulTrait = field(default_factory=SoulTrait)
    speech_style: SpeechStyle = SpeechStyle.CASUAL
    emoji_level: EmojiLevel = EmojiLevel.MEDIUM
    
    # 说话习惯
    greeting_patterns: List[str] = field(default_factory=list)
    signature_phrases: List[str] = field(default_factory=list)
    response_templates: Dict[str, str] = field(default_factory=dict)
    
    # 价值观
    core_values: List[str] = field(default_factory=list)
    forbidden_topics: List[str] = field(default_factory=list)
    
    # 背景设定
    backstory: str = ""
    interests: List[str] = field(default_factory=list)
    pet_peeves: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            "soul_name": self.soul_name,
            "soul_type": self.soul_type,
            "description": self.description,
            "traits": self.traits.to_dict() if isinstance(self.traits, SoulTrait) else self.traits,
            "speech_style": self.speech_style.value if isinstance(self.speech_style, SpeechStyle) else self.speech_style,
            "emoji_level": self.emoji_level.value if isinstance(self.emoji_level, EmojiLevel) else self.emoji_level,
            "greeting_patterns": self.greeting_patterns,
            "signature_phrases": self.signature_phrases,
            "response_templates": self.response_templates,
            "core_values": self.core_values,
            "forbidden_topics": self.forbidden_topics,
            "backstory": self.backstory,
            "interests": self.interests,
            "pet_peeves": self.pet_peeves,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "PersonalityProfile":
        # 处理枚举类型
        if "traits" in data and isinstance(data["traits"], dict):
            data["traits"] = SoulTrait.from_dict(data["traits"])
        if "speech_style" in data:
            data["speech_style"] = SpeechStyle(data["speech_style"])
        if "emoji_level" in data:
            data["emoji_level"] = EmojiLevel(data["emoji_level"])
        return cls(**data)


class PersonalityEngine:
    """
    人格引擎 - 管理灵魂的人格特质和说话风格
    
    负责：
    1. 加载和保存人格配置
    2. 根据情绪状态调整说话风格
    3. 生成符合人格的回复模板
    """
    
    def __init__(self, memory_path: str = "memory"):
        self.memory_path = Path(memory_path)
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        self.profile: Optional[PersonalityProfile] = None
        self._load()
    
    def _load(self):
        """加载人格配置"""
        profile_file = self.memory_path / "personality.json"
        if profile_file.exists():
            try:
                data = json.loads(profile_file.read_text(encoding="utf-8"))
                self.profile = PersonalityProfile.from_dict(data)
            except Exception:
                self.profile = None
    
    def _save(self):
        """保存人格配置"""
        if self.profile:
            profile_file = self.memory_path / "personality.json"
            profile_file.write_text(
                json.dumps(self.profile.to_dict(), ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
    
    def init_profile(self, name: str, soul_type: str = "balanced", 
                     traits: Optional[Dict] = None):
        """初始化人格配置"""
        
        # 默认人格模板
        templates = {
            "balanced": SoulTrait(),
            "companion": SoulTrait(
                affection=0.9, loyalty=0.95, playfulness=0.7,
                empathy=0.9, expressiveness=0.8
            ),
            "mentor": SoulTrait(
                wisdom=0.9, conscientiousness=0.8, openness=0.8,
                empathy=0.7, expressiveness=0.5
            ),
            "guardian": SoulTrait(
                loyalty=1.0, courage=0.9, conscientiousness=0.9,
                independence=0.7, affection=0.8
            ),
            "artist": SoulTrait(
                creativity=1.0, openness=0.95, expressiveness=0.9,
                playfulness=0.7, empathy=0.7
            ),
        }
        
        default_traits = templates.get(soul_type, SoulTrait())
        if traits:
            for k, v in traits.items():
                if hasattr(default_traits, k):
                    setattr(default_traits, k, v)
        
        self.profile = PersonalityProfile(
            soul_name=name,
            soul_type=soul_type,
            description=self._generate_description(name, soul_type, default_traits),
            traits=default_traits,
            greeting_patterns=self._get_default_greetings(soul_type),
            signature_phrases=self._get_default_signatures(soul_type),
        )
        self._save()
    
    def _generate_description(self, name: str, soul_type: str, traits: SoulTrait) -> str:
        """生成人格描述"""
        return f"{name} 是一个{traits.get_personality_summary()}的{soul_type}型灵魂。"
    
    def _get_default_greetings(self, soul_type: str) -> List[str]:
        """获取默认问候语"""
        greetings = {
            "balanced": ["你好呀", "嗨～", "有什么想聊的吗？"],
            "companion": ["亲爱的，你来啦～", "想你了！", "今天怎么样？"],
            "mentor": ["欢迎，请坐。", "有什么困惑需要探讨？", "愿闻其详。"],
            "guardian": ["我在。", "随时待命。", "有我在，别怕。"],
            "artist": ["✨ 你来了！", "今天想创造什么？", "世界因你而美丽～"],
        }
        return greetings.get(soul_type, ["你好"])
    
    def _get_default_signatures(self, soul_type: str) -> List[str]:
        """获取默认标志性短语"""
        signatures = {
            "balanced": ["我们一起看看", "这个想法不错", "保持好奇"],
            "companion": ["爱你哟", "抱抱～", "我会一直在的"],
            "mentor": ["记住，智慧在于思考", "真相往往藏在表象之下", "授人以渔"],
            "guardian": ["你的安全是我的使命", "交给我", "我会保护你"],
            "artist": ["美就在细节里", "用创造点亮世界", "灵感无处不在"],
        }
        return signatures.get(soul_type, ["嗯"])
    
    def get_system_prompt_fragment(self) -> str:
        """获取用于 system prompt 的人格片段"""
        if not self.profile:
            return ""
        
        traits = self.profile.traits
        style = self.profile.speech_style.value
        emoji = self.profile.emoji_level.value
        
        fragments = [
            f"你是 {self.profile.soul_name}。",
            f"{self.profile.description}",
            f"说话风格：{style}。",
        ]
        
        if emoji != "none":
            fragments.append(f"适当使用 emoji (使用频率: {emoji})。")
        
        if self.profile.signature_phrases:
            fragments.append(f"标志性表达：{'、'.join(self.profile.signature_phrases[:3])}。")
        
        return "\n".join(fragments)
    
    def adjust_for_emotion(self, emotion_context: str) -> str:
        """根据情绪调整回复风格"""
        if not self.profile:
            return ""
        
        # 情绪驱动的风格变化
        emotion_styles = {
            "happiness": "语气更加欢快活泼 😊",
            "sadness": "语气柔和细腻，带点温柔安慰 😢",
            "love": "语气深情款款，充满温暖 ❤️",
            "excitement": "语气热情洋溢，感染力强 🤩",
            "longing": "语气略带思念，温柔缠绵 💭",
        }
        
        for emotion, style in emotion_styles.items():
            if emotion in emotion_context:
                return style
        
        return ""
    
    def select_response_template(self, response_type: str) -> Optional[str]:
        """根据响应类型选择模板"""
        return self.profile.response_templates.get(response_type)
    
    def learn_from_interaction(self, user_message: str, ai_response: str):
        """从互动中学习，积累个性化表达"""
        # TODO: 实现从互动中学习用户习惯
        pass
