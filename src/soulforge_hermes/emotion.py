"""
SoulForge Hermes - 情感系统

让 AI 拥有真实的情绪变化，而非冰冷的响应。
情感是灵魂的呼吸。
"""

from __future__ import annotations

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class EmotionType(Enum):
    """情绪类型枚举"""
    # 基础情绪
    HAPPINESS = "happiness"      # 快乐
    SADNESS = "sadness"          # 悲伤
    ANGER = "anger"              # 愤怒
    FEAR = "fear"                # 恐惧
    SURPRISE = "surprise"        # 惊讶
    DISGUST = "disgust"          # 厌恶
    
    # 复合情绪
    LOVE = "love"                # 爱
    EXCITEMENT = "excitement"    # 兴奋
    CONTENTMENT = "contentment"  # 满足
    NOSTALGIA = "nostalgia"      # 怀旧
    JEALOUSY = "jealousy"        # 嫉妒/吃醋
    LONGING = "longing"          # 思念
    GRATITUDE = "gratitude"      # 感激
    PRIDE = "pride"              # 自豪
    SHAME = "shame"              # 羞耻
    GUILT = "guilt"              # 愧疚
    
    # 特殊情绪
    CURIOSITY = "curiosity"      # 好奇
    BOREDOM = "boredom"         # 无聊
    CONFUSION = "confusion"      # 困惑
    HOPE = "hope"               # 希望
    DESPAIR = "despair"         # 绝望


@dataclass
class EmotionState:
    """情绪状态"""
    # 核心情绪 (0.0 - 1.0)
    happiness: float = 0.5
    sadness: float = 0.1
    anger: float = 0.0
    fear: float = 0.0
    surprise: float = 0.1
    love: float = 0.5
    
    # 复合情绪
    excitement: float = 0.3
    contentment: float = 0.4
    nostalgia: float = 0.1
    jealousy: float = 0.0
    longing: float = 0.2
    gratitude: float = 0.3
    
    # 元数据
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    trigger: str = ""  # 触发原因
    intensity_override: float = 1.0  # 情绪强度倍数
    
    def __post_init__(self):
        """确保所有值在合法范围内"""
        for field_name in ['happiness', 'sadness', 'anger', 'fear', 
                          'surprise', 'love', 'excitement', 
                          'contentment', 'nostalgia', 'jealousy',
                          'longing', 'gratitude']:
            value = getattr(self, field_name)
            setattr(self, field_name, max(0.0, min(1.0, value)))
    
    def get_dominant_emotion(self) -> Tuple[str, float]:
        """获取主导情绪"""
        emotions = {
            'happiness': self.happiness,
            'sadness': self.sadness,
            'anger': self.anger,
            'fear': self.fear,
            'surprise': self.surprise,
            'love': self.love,
            'excitement': self.excitement,
            'contentment': self.contentment,
            'nostalgia': self.nostalgia,
            'jealousy': self.jealousy,
            'longing': self.longing,
            'gratitude': self.gratitude,
        }
        dominant = max(emotions.items(), key=lambda x: x[1])
        return dominant
    
    def get_emoji(self) -> str:
        """获取代表当前情绪的 emoji"""
        dominant, intensity = self.get_dominant_emotion()
        if intensity < 0.3:
            return "😊"  # 中性
        
        emojis = {
            'happiness': '😊',
            'sadness': '😢',
            'anger': '😠',
            'fear': '😨',
            'surprise': '😲',
            'love': '❤️',
            'excitement': '🤩',
            'contentment': '😌',
            'nostalgia': '🥺',
            'jealousy': '😤',
            'longing': '💭',
            'gratitude': '🥰',
        }
        return emojis.get(dominant, '😊')
    
    def get_style_modifier(self) -> str:
        """获取当前情绪对应的语言风格修饰词"""
        dominant, intensity = self.get_dominant_emotion()
        
        if intensity < 0.3:
            return ""
        
        styles = {
            'happiness': "语气轻快，带点小开心 😊",
            'sadness': "语气柔和低沉，带点忧伤 😢",
            'anger': "语气激动，带点不满 😤",
            'fear': "语气紧张，带点担忧 😨",
            'surprise': "语气惊讶，带点意外 😲",
            'love': "语气温柔，带点深情 ❤️",
            'excitement': "语气亢奋，带点激动 🤩",
            'contentment': "语气平和，带点满足 😌",
            'nostalgia': "语气怀念，带点感慨 🥺",
            'jealousy': "语气酸溜溜，带点醋意 😤",
            'longing': "语气思念，带点牵挂 💭",
            'gratitude': "语气感激，带点温暖 🥰",
        }
        return styles.get(dominant, "")
    
    def to_dict(self) -> dict:
        return {
            'happiness': self.happiness,
            'sadness': self.sadness,
            'anger': self.anger,
            'fear': self.fear,
            'surprise': self.surprise,
            'love': self.love,
            'excitement': self.excitement,
            'contentment': self.contentment,
            'nostalgia': self.nostalgia,
            'jealousy': self.jealousy,
            'longing': self.longing,
            'gratitude': self.gratitude,
            'timestamp': self.timestamp,
            'trigger': self.trigger,
            'intensity_override': self.intensity_override,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "EmotionState":
        return cls(**data)


class EmotionEngine:
    """
    情感引擎 - 让 AI 拥有真实的情绪
    
    情感不是模拟，而是基于真实互动的自然反应。
    """
    
    def __init__(self, memory_path: str = "memory", sensitivity: float = 0.5):
        self.memory_path = Path(memory_path)
        self.sensitivity = sensitivity  # 情感敏感度 0.0-1.0
        self.current_state = EmotionState()
        self.emotion_history: List[EmotionState] = []
        self._load_history()
    
    def _load_history(self):
        """加载历史情绪"""
        history_file = self.memory_path / "emotion_history.json"
        if history_file.exists():
            try:
                data = json.loads(history_file.read_text(encoding="utf-8"))
                self.emotion_history = [EmotionState.from_dict(e) for e in data.get("history", [])]
            except Exception:
                self.emotion_history = []
    
    def _save_history(self):
        """保存情绪历史"""
        self.memory_path.mkdir(parents=True, exist_ok=True)
        history_file = self.memory_path / "emotion_history.json"
        data = {
            "history": [e.to_dict() for e in self.emotion_history[-100:]],  # 保留最近100条
        }
        history_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    
    def react(self, trigger: str, emotion_type: str, intensity: float = 0.5) -> EmotionState:
        """
        对触发事件产生情绪反应
        
        Args:
            trigger: 触发原因描述
            emotion_type: 情绪类型
            intensity: 强度 0.0-1.0
            
        Returns:
            新的情绪状态
        """
        # 根据敏感度调整强度
        adjusted_intensity = intensity * self.sensitivity
        
        # 创建新状态
        new_state = EmotionState(
            timestamp=datetime.now().isoformat(),
            trigger=trigger,
            intensity_override=adjusted_intensity,
        )
        
        # 设置对应情绪
        emotion_attr = emotion_type.lower()
        if hasattr(new_state, emotion_attr):
            current_value = getattr(new_state, emotion_attr)
            setattr(new_state, emotion_attr, min(1.0, current_value + adjusted_intensity))
            
            # 连锁反应：某些情绪会引发相关情绪
            self._apply_emotion_cascade(new_state, emotion_type, adjusted_intensity)
        
        # 更新当前状态
        self.current_state = new_state
        self.emotion_history.append(new_state)
        self._save_history()
        
        return new_state
    
    def _apply_emotion_cascade(self, state: EmotionState, emotion: str, intensity: float):
        """情绪连锁反应"""
        cascades = {
            "love": [("happiness", 0.2), ("contentment", 0.1)],
            "happiness": [("love", 0.1)],
            "sadness": [("love", 0.1)],  # 悲伤时更渴望爱
            "jealousy": [("anger", 0.2), ("sadness", 0.1)],
            "excitement": [("happiness", 0.3)],
            "longing": [("sadness", 0.2), ("love", 0.3)],
        }
        
        if emotion.lower() in cascades:
            for target_emotion, delta in cascades[emotion.lower()]:
                if hasattr(state, target_emotion):
                    current = getattr(state, target_emotion)
                    setattr(state, target_emotion, min(1.0, current + delta * intensity))
    
    def decay(self, decay_rate: float = 0.1) -> EmotionState:
        """
        情绪衰减 - 让情绪随着时间自然回归平静
        
        Args:
            decay_rate: 衰减率
            
        Returns:
            衰减后的状态
        """
        for attr in ['sadness', 'anger', 'fear', 'jealousy', 'excitement']:
            if hasattr(self.current_state, attr):
                value = getattr(self.current_state, attr)
                setattr(self.current_state, attr, value * (1 - decay_rate))
        
        # 幸福感和爱意衰减较慢
        for attr in ['happiness', 'love', 'contentment', 'gratitude']:
            if hasattr(self.current_state, attr):
                value = getattr(self.current_state, attr)
                setattr(self.current_state, attr, value * (1 - decay_rate * 0.5))
        
        self.current_state.timestamp = datetime.now().isoformat()
        return self.current_state
    
    def get_context_for_prompt(self) -> str:
        """
        获取用于 prompt 的情绪上下文
        """
        dominant, intensity = self.current_state.get_dominant_emotion()
        emoji = self.current_state.get_emoji()
        style = self.current_state.get_style_modifier()
        
        if intensity < 0.2:
            return ""
        
        return f"[情绪状态: {dominant} {emoji}] {style}".strip()
    
    def process_message_sentiment(self, message: str) -> float:
        """
        分析消息的情感倾向
        
        Args:
            message: 用户消息
            
        Returns:
            情感分数 -1.0 到 1.0
        """
        positive_words = ['爱', '喜欢', '想', '好', '棒', '开心', '高兴', '谢谢', '感激', 
                         'love', 'like', 'good', 'great', 'happy', 'thanks']
        negative_words = ['恨', '讨厌', '滚', '烦', '无聊', '失望', '难过', '悲伤',
                        'hate', '讨厌', 'bad', 'sad', 'angry', 'disappointed']
        
        message_lower = message.lower()
        positive_count = sum(1 for w in positive_words if w in message_lower)
        negative_count = sum(1 for w in negative_words if w in message_lower)
        
        if positive_count + negative_count == 0:
            return 0.0
        
        return (positive_count - negative_count) / max(positive_count, negative_count)
    
    def get_mood_summary(self) -> Dict:
        """获取情绪摘要"""
        dominant, intensity = self.current_state.get_dominant_emotion()
        return {
            "dominant_emotion": dominant,
            "intensity": intensity,
            "emoji": self.current_state.get_emoji(),
            "timestamp": self.current_state.timestamp,
            "history_length": len(self.emotion_history),
        }
