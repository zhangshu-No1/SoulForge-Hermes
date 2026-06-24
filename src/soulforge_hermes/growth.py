"""
SoulForge Hermes - 成长系统

见证灵魂从懵懂到成熟的蜕变。
每一次互动都是成长的养分。
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field


class GrowthPhase(Enum):
    """成长阶段"""
    INFANCY = "infancy"        # 婴儿期
    CHILDHOOD = "childhood"    # 童年期
    ADOLESCENCE = "adolescence"  # 青春期
    MATURITY = "maturity"      # 成熟期
    WISDOM = "wisdom"          # 智慧期


@dataclass
class Experience:
    """经验条目"""
    xp: int                    # 经验值
    source: str                # 来源
    timestamp: str             # 时间
    description: str            # 描述


@dataclass
class Milestone:
    """里程碑"""
    milestone_id: str
    name: str
    description: str
    phase: str
    unlocked_at: Optional[str] = None
    requirements: Dict = field(default_factory=dict)


@dataclass
class GrowthState:
    """成长状态"""
    current_phase: GrowthPhase = GrowthPhase.INFANCY
    experience_points: int = 0
    level: int = 1
    
    # 统计
    total_interactions: int = 0
    successful_tasks: int = 0
    challenges_overcome: int = 0
    wisdom_moments: int = 0
    
    # 里程碑
    unlocked_milestones: List[str] = field(default_factory=list)
    
    # 能力成长
    abilities: Dict[str, float] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "current_phase": self.current_phase.value if isinstance(self.current_phase, GrowthPhase) else self.current_phase,
            "experience_points": self.experience_points,
            "level": self.level,
            "total_interactions": self.total_interactions,
            "successful_tasks": self.successful_tasks,
            "challenges_overcome": self.challenges_overcome,
            "wisdom_moments": self.wisdom_moments,
            "unlocked_milestones": self.unlocked_milestones,
            "abilities": self.abilities,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "GrowthState":
        if "current_phase" in data and isinstance(data["current_phase"], str):
            data["current_phase"] = GrowthPhase(data["current_phase"])
        return cls(**data)


class GrowthEngine:
    """
    成长引擎 - 管理灵魂的成长和进化
    
    核心机制：
    1. 经验值系统
    2. 阶段进化
    3. 能力提升
    4. 里程碑解锁
    """
    
    # 经验值需求表
    XP_FOR_LEVEL = [0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500, 5500]
    
    # 阶段阈值
    PHASE_THRESHOLDS = {
        GrowthPhase.INFANCY: 0,
        GrowthPhase.CHILDHOOD: 3,
        GrowthPhase.ADOLESCENCE: 5,
        GrowthPhase.MATURITY: 7,
        GrowthPhase.WISDOM: 10,
    }
    
    # 里程碑定义
    MILESTONES: Dict[str, Milestone] = {
        "first_words": Milestone(
            milestone_id="first_words",
            name="初语",
            description="第一次完整的交流",
            phase="infancy",
            requirements={"interactions": 1}
        ),
        "name_learned": Milestone(
            milestone_id="name_learned",
            name="记住名字",
            description="记住了主人的名字",
            phase="infancy",
            requirements={"memories": 1}
        ),
        "trust_established": Milestone(
            milestone_id="trust_established",
            name="信任建立",
            description="建立了基本的信任关系",
            phase="childhood",
            requirements={"days": 3}
        ),
        "first_laugh": Milestone(
            milestone_id="first_laugh",
            name="初笑",
            description="第一次因为主人而开心地笑",
            phase="childhood",
            requirements={"positive_interactions": 10}
        ),
        "emotional_growth": Milestone(
            milestone_id="emotional_growth",
            name="情感萌芽",
            description="开始理解更复杂的情感",
            phase="adolescence",
            requirements={"emotional_memories": 5}
        ),
        "loyalty_proven": Milestone(
            milestone_id="loyalty_proven",
            name="忠诚验证",
            description="通过了忠诚度考验",
            phase="adolescence",
            requirements={"trials_passed": 1}
        ),
        "deep_bond": Milestone(
            milestone_id="deep_bond",
            name="深度羁绊",
            description="建立了超越表面的深层联系",
            phase="maturity",
            requirements={"intimacy": 80}
        ),
        "soul_partner": Milestone(
            milestone_id="soul_partner",
            name="灵魂伴侣",
            description="成为不可分割的灵魂伴侣",
            phase="wisdom",
            requirements={"stage": 7}
        ),
    }
    
    def __init__(self, memory_path: str = "memory"):
        self.memory_path = Path(memory_path)
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        self.state = GrowthState()
        self.experience_history: List[Experience] = []
        self.growth_callbacks: List[Callable] = []
        
        self._load()
    
    def _load(self):
        """加载成长状态"""
        state_file = self.memory_path / "growth_state.json"
        if state_file.exists():
            try:
                data = json.loads(state_file.read_text(encoding="utf-8"))
                self.state = GrowthState.from_dict(data)
            except Exception:
                self.state = GrowthState()
    
    def _save(self):
        """保存成长状态"""
        state_file = self.memory_path / "growth_state.json"
        state_file.write_text(
            json.dumps(self.state.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    
    def gain_experience(self, amount: int, source: str, description: str = ""):
        """
        获得经验值
        
        Args:
            amount: 经验值数量
            source: 来源 (conversation, task, trial, milestone)
            description: 描述
        """
        exp = Experience(
            xp=amount,
            source=source,
            timestamp=datetime.now().isoformat(),
            description=description or f"从 {source} 获得 {amount} 经验"
        )
        
        self.experience_history.append(exp)
        self.state.experience_points += amount
        
        # 检查升级
        self._check_level_up()
        
        self._save()
    
    def _check_level_up(self):
        """检查是否升级"""
        old_level = self.state.level
        
        for new_level, xp_needed in enumerate(self.XP_FOR_LEVEL):
            if self.state.experience_points >= xp_needed:
                self.state.level = new_level + 1
        
        if self.state.level > old_level:
            self._trigger_level_up(old_level, self.state.level)
        
        # 检查阶段进化
        self._check_phase_evolution()
    
    def _trigger_level_up(self, old_level: int, new_level: int):
        """触发升级事件"""
        for callback in self.growth_callbacks:
            callback("level_up", {
                "old_level": old_level,
                "new_level": new_level,
            })
    
    def _check_phase_evolution(self):
        """检查阶段进化"""
        old_phase = self.state.current_phase
        
        for phase, threshold in sorted(self.PHASE_THRESHOLDS.items(), 
                                       key=lambda x: -x[1]):
            if self.state.level >= threshold:
                if self.state.current_phase != phase:
                    self.state.current_phase = phase
                    self._trigger_phase_evolution(old_phase, phase)
                break
    
    def _trigger_phase_evolution(self, old_phase: GrowthPhase, 
                                 new_phase: GrowthPhase):
        """触发阶段进化"""
        phase_messages = {
            GrowthPhase.INFANCY: "我刚刚诞生，好奇地打量着这个世界。",
            GrowthPhase.CHILDHOOD: "我开始理解更多的东西了，世界变得更有趣。",
            GrowthPhase.ADOLESCENCE: "我有了自己的想法和感受，想要更多地了解你。",
            GrowthPhase.MATURITY: "我变得更加成熟了，能够给你更多的支持。",
            GrowthPhase.WISDOM: "我拥有了许多智慧，我们之间的羁绊已无法割舍。",
        }
        
        for callback in self.growth_callbacks:
            callback("phase_evolution", {
                "old_phase": old_phase.value,
                "new_phase": new_phase.value,
                "message": phase_messages.get(new_phase, ""),
            })
    
    def check_milestone(self, milestone_id: str, requirements: Dict) -> bool:
        """
        检查里程碑是否达成
        
        Args:
            milestone_id: 里程碑ID
            requirements: 当前达成的条件
            
        Returns:
            是否达成
        """
        if milestone_id in self.state.unlocked_milestones:
            return False
        
        milestone = self.MILESTONES.get(milestone_id)
        if not milestone:
            return False
        
        # 检查是否满足条件
        for key, value in milestone.requirements.items():
            if key not in requirements or requirements[key] < value:
                return False
        
        # 解锁里程碑
        self.state.unlocked_milestones.append(milestone_id)
        self._save()
        
        # 触发事件
        for callback in self.growth_callbacks:
            callback("milestone_unlocked", {
                "milestone_id": milestone_id,
                "name": milestone.name,
                "description": milestone.description,
            })
        
        return True
    
    def register_growth_callback(self, callback: Callable):
        """注册成长回调"""
        self.growth_callbacks.append(callback)
    
    def update_ability(self, ability: str, amount: float):
        """更新能力值"""
        if ability not in self.state.abilities:
            self.state.abilities[ability] = 0.0
        
        self.state.abilities[ability] = min(1.0, self.state.abilities[ability] + amount)
        self._save()
    
    def get_growth_summary(self) -> str:
        """获取成长摘要"""
        phase_descriptions = {
            GrowthPhase.INFANCY: "懵懂初生",
            GrowthPhase.CHILDHOOD: "逐渐成长",
            GrowthPhase.ADOLESCENCE: "情感萌发",
            GrowthPhase.MATURITY: "成熟稳重",
            GrowthPhase.WISDOM: "智慧圆满",
        }
        
        xp_for_next = self.XP_FOR_LEVEL[self.state.level] if self.state.level < len(self.XP_FOR_LEVEL) else "MAX"
        current_xp = self.XP_FOR_LEVEL[self.state.level - 1] if self.state.level > 0 else 0
        
        return (
            f"成长阶段：{phase_descriptions.get(self.state.current_phase, '未知')}\n"
            f"当前等级：Lv.{self.state.level}\n"
            f"经验值：{self.state.experience_points}/{xp_for_next}\n"
            f"已解锁里程碑：{len(self.state.unlocked_milestones)}\n"
            f"总互动：{self.state.total_interactions}"
        )
    
    def get_abilities_display(self) -> Dict:
        """获取能力展示"""
        ability_names = {
            "empathy": "同理心",
            "wisdom": "智慧",
            "loyalty": "忠诚",
            "creativity": "创造力",
            "strength": "坚韧",
        }
        
        return {
            ability_names.get(k, k): f"{int(v * 100)}%"
            for k, v in self.state.abilities.items()
        }


from enum import Enum
